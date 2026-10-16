/**
 * MalyPetShop - Capa de Servicio API con Conexión a Supabase Cloud
 * Proyecto: MalyPetShop (https://vbhkqmshoouguhopyxli.supabase.co)
 */

window.SUPABASE_CONFIG = {
  url: "https://vbhkqmshoouguhopyxli.supabase.co",
  anonKey: "sb_publishable_yeRE6YC5IteDHTIrip6Teg_vrwQyO3M"
};

window.API = {
  baseUrl: (typeof window !== 'undefined' && window.location && window.location.origin && window.location.origin.includes('http')) 
           ? window.location.origin : 'http://localhost:8000',
  isBackendConnected: false,
  isSupabaseConnected: false,
  supabaseClient: null,
  cachedCategories: null,
  cachedBrands: null,

  init() {
    try {
      if (typeof window !== 'undefined' && window.supabase && typeof window.supabase.createClient === 'function') {
        this.supabaseClient = window.supabase.createClient(window.SUPABASE_CONFIG.url, window.SUPABASE_CONFIG.anonKey);
        this.isSupabaseConnected = true;
        console.log('✅ [Supabase] Cliente inicializado con MalyPetShop Cloud.');
      } else {
        console.log('ℹ️ [Supabase] Modo híbrido activo.');
      }
    } catch (e) {
      console.warn('⚠️ [Supabase] Error en init:', e);
    }
  },

  async checkHealth() {
    if (!this.supabaseClient) this.init();

    // 1. Probar Supabase Cloud
    if (this.supabaseClient) {
      try {
        const { data, error } = await this.supabaseClient.from('store_settings').select('key').limit(1);
        if (!error && data) {
          this.isSupabaseConnected = true;
          return {
            status: "healthy",
            service: "Supabase Cloud Database (PostgreSQL)",
            connected: true
          };
        }
      } catch (e) {}
    }

    // 2. Probar Backend local Python si está activo
    try {
      const res = await fetch(`${this.baseUrl}/api/health`, { method: 'GET', headers: { 'Accept': 'application/json' } });
      if (res.ok) {
        const data = await res.json();
        this.isBackendConnected = true;
        return data;
      }
    } catch (e) {
      this.isBackendConnected = false;
    }
    return null;
  },

  formatSupabaseProduct(p) {
    // Variantes
    const rawVariants = Array.isArray(p.product_variants) ? p.product_variants : [];
    const variants = rawVariants.sort((a, b) => (Number(a.weight_kg) || 0) - (Number(b.weight_kg) || 0));
    const presentations = variants.map(v => v.presentation_name);
    const prices = variants.map(v => Number(v.sale_price));
    const list_prices = variants.map(v => Number(v.list_price || Math.round(v.sale_price * 1.15)));
    const costs = variants.map(v => Number(v.cost_price || 0));

    // Categoría
    let catName = 'General';
    let catSlug = 'perros';
    if (p.categories) {
      if (Array.isArray(p.categories) && p.categories.length > 0) {
        catName = p.categories[0].name || catName;
        catSlug = p.categories[0].slug || catSlug;
      } else if (typeof p.categories === 'object') {
        catName = p.categories.name || catName;
        catSlug = p.categories.slug || catSlug;
      }
    }

    // Marca
    let brandName = 'Maly Petshop';
    if (p.brands) {
      if (Array.isArray(p.brands) && p.brands.length > 0) {
        brandName = p.brands[0].name || brandName;
      } else if (typeof p.brands === 'object') {
        brandName = p.brands.name || brandName;
      }
    }

    return {
      id: p.id,
      name: p.name,
      slug: p.slug,
      description: p.description || '',
      desc: p.description || '',
      pet_type: p.pet_type || 'ambos',
      subcat: p.subcat || 'general',
      breed_size: p.breed_size || 'todas',
      badge: p.badge || '',
      image_url: p.image_url || '',
      is_featured: p.is_featured ? 1 : 0,
      featured: Boolean(p.is_featured),
      is_promo: p.is_promo ? 1 : 0,
      promo: Boolean(p.is_promo),
      promo_tag: p.promo_tag || '',
      category_name: catName,
      category_slug: catSlug,
      category: catSlug,
      brand_name: brandName,
      brand: brandName,
      variants: variants,
      presentations: presentations.length ? presentations : ['Única'],
      prices: prices.length ? prices : [0],
      list_prices: list_prices.length ? list_prices : [0],
      costs: costs.length ? costs : [0]
    };
  },

  async getProducts(params = {}) {
    if (!this.supabaseClient) this.init();

    // RUTA 1: Consultar a Supabase Cloud
    if (this.supabaseClient) {
      try {
        let query = this.supabaseClient
          .from('products')
          .select('*, categories(name, slug), brands(name), product_variants(*)')
          .eq('active', true)
          .order('is_featured', { ascending: false })
          .order('id', { ascending: true });

        if (params.category && params.category !== 'todos') {
          if (params.category === 'promociones') {
            query = query.eq('is_promo', true);
          }
        }

        if (params.pet_type && params.pet_type !== 'todos') {
          query = query.or(`pet_type.eq.${params.pet_type},pet_type.eq.ambos`);
        }

        if (params.subcat && params.subcat !== 'todas') {
          query = query.eq('subcat', params.subcat);
        }

        if (params.breed_size && params.breed_size !== 'todas') {
          query = query.or(`breed_size.eq.${params.breed_size},breed_size.eq.todas`);
        }

        if (params.promoOnly) {
          query = query.eq('is_promo', true);
        }

        // Búsqueda inteligente SQL LIKE tokenizada aplicada a los productos obtenidos

        const { data, error } = await query;
        if (!error && Array.isArray(data) && data.length > 0) {
          let formatted = data.map(p => this.formatSupabaseProduct(p));
          if (params.category && params.category !== 'todos' && params.category !== 'promociones') {
            formatted = formatted.filter(p => p.category_slug === params.category);
          }
          if (params.brand && params.brand !== 'todas') {
            formatted = formatted.filter(p => p.brand_name.toLowerCase() === params.brand.toLowerCase());
          }
          if (params.search) {
            formatted = this.searchProductsLike(params.search, formatted);
          }
          console.log(`✅ [Supabase] ${formatted.length} productos cargados desde la nube.`);
          return formatted;
        } else if (error) {
          console.warn('[Supabase] Aviso en consulta:', error.message);
        }
      } catch (err) {
        console.warn('[Supabase] Error en getProducts:', err);
      }
    }

    // RUTA 2: Servidor local Python (cuando corrés python run.py)
    try {
      const q = new URLSearchParams();
      if (params.category && params.category !== 'todos') q.append('category', params.category);
      if (params.pet_type && params.pet_type !== 'todos') q.append('pet_type', params.pet_type);
      if (params.subcat && params.subcat !== 'todas') q.append('subcat', params.subcat);
      if (params.breed_size && params.breed_size !== 'todas') q.append('breed_size', params.breed_size);
      if (params.brand && params.brand !== 'todas') q.append('brand', params.brand);
      if (params.promoOnly) q.append('is_promo', 'true');
      if (params.search) q.append('search', params.search);

      const res = await fetch(`${this.baseUrl}/api/products?${q.toString()}`);
      if (res.ok) {
        const localData = await res.json();
        if (Array.isArray(localData) && localData.length > 0) {
          this.isBackendConnected = true;
          console.log(`✅ [Local Server] ${localData.length} productos cargados desde el servidor local.`);
          return localData;
        }
      }
    } catch (e) {}

    // RUTA 3: Catálogo estático empaquetado (reserva segura)
    console.log('ℹ️ [Catálogo] Usando catálogo base local.');
    return this.filterLocalProducts(params);
  },

  async updateProductImage(productId, imageUrl) {
    if (!this.supabaseClient) this.init();

    if (this.supabaseClient) {
      try {
        await this.supabaseClient.from('products').update({ image_url: imageUrl }).eq('id', productId);
      } catch (e) {}
    }

    if (this.isBackendConnected) {
      try {
        await fetch(`${this.baseUrl}/api/products/${productId}/image`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_url: imageUrl })
        });
      } catch (e) {}
    }

    const custom = JSON.parse(localStorage.getItem('petshop_custom_images') || '{}');
    custom[productId] = imageUrl;
    localStorage.setItem('petshop_custom_images', JSON.stringify(custom));
    
    // 3. Actualizar inmediatamente en el catálogo en memoria
    const source = (typeof window !== 'undefined' && window.LOCAL_CATALOG) || (typeof LOCAL_CATALOG !== 'undefined' && LOCAL_CATALOG);
    if (source && Array.isArray(source)) {
      const p = source.find(item => item.id === productId);
      if (p) {
        if (productData.name) p.name = productData.name;
        if (productData.description !== undefined) p.description = productData.description;
        if (productData.image_url) p.image_url = productData.image_url;
        if (productData.badge !== undefined) p.badge = productData.badge;
        if (productData.is_promo !== undefined) p.is_promo = productData.is_promo ? 1 : 0;
        if (productData.is_featured !== undefined) p.is_featured = productData.is_featured ? 1 : 0;
        if (productData.variants && productData.variants.length > 0) {
          p.variants = productData.variants;
          p.presentations = productData.variants.map(v => v.presentation_name);
          p.costs = productData.variants.map(v => Number(v.cost_price));
          p.prices = productData.variants.map(v => Number(v.sale_price));
          p.list_prices = productData.variants.map(v => Number(v.list_price));
        }
      }
    }
    return true;
  },

  async updateProduct(productId, productData) {
    if (!this.supabaseClient) this.init();

    if (this.supabaseClient) {
      try {
        const fields = {};
        if (productData.name) fields.name = productData.name;
        if (productData.description !== undefined) fields.description = productData.description;
        if (productData.pet_type) fields.pet_type = productData.pet_type;
        if (productData.subcat) fields.subcat = productData.subcat;
        if (productData.breed_size) fields.breed_size = productData.breed_size;
        if (productData.badge !== undefined) fields.badge = productData.badge;
        if (productData.image_url) fields.image_url = productData.image_url;
        if (productData.is_featured !== undefined) fields.is_featured = Boolean(productData.is_featured);
        if (productData.is_promo !== undefined) fields.is_promo = Boolean(productData.is_promo);
        if (productData.promo_tag !== undefined) fields.promo_tag = productData.promo_tag;

        if (Object.keys(fields).length > 0) {
          await this.supabaseClient.from('products').update(fields).eq('id', productId);
        }

        if (productData.variants && Array.isArray(productData.variants) && productData.variants.length > 0) {
          // 1. Eliminar variantes previas de este producto en Supabase
          await this.supabaseClient.from('product_variants').delete().eq('product_id', productId);

          // 2. Insertar las variantes con los nuevos costos y precios calculados
          const newVariants = productData.variants.map((v, idx) => ({
            product_id: productId,
            presentation_name: v.presentation_name || 'Unidad',
            weight_kg: Number(v.weight_kg || 1.0),
            cost_price: Number(v.cost_price || 1000.0),
            margin_percent: Number(v.margin_percent || 25.0),
            sale_price: Number(v.sale_price || Math.round(Number(v.cost_price || 1000) * (1 + (v.margin_percent || 25) / 100))),
            list_price: Number(v.list_price || (Boolean(productData.is_promo) ? Math.round(Number(v.sale_price) * 1.15) : Number(v.sale_price))),
            stock_qty: 100,
            sku: `MALY-${productId}-${idx + 1}`,
            is_default: idx === 0
          }));

          const { error: insErr } = await this.supabaseClient.from('product_variants').insert(newVariants);
          if (insErr) {
            console.error('[Supabase Error] al insertar variantes actualizadas:', insErr);
          } else {
            console.log(`✅ [Supabase] ${newVariants.length} variantes (costos y precios) guardadas en la nube para producto ${productId}`);
          }
        }
      } catch (e) {}
    }

    if (this.isBackendConnected) {
      try {
        await fetch(`${this.baseUrl}/api/products/${productId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(productData)
        });
      } catch (e) {}
    }

    
    // 3. Actualizar inmediatamente en el catálogo en memoria
    const source = (typeof window !== 'undefined' && window.LOCAL_CATALOG) || (typeof LOCAL_CATALOG !== 'undefined' && LOCAL_CATALOG);
    if (source && Array.isArray(source)) {
      const p = source.find(item => item.id === productId);
      if (p) {
        if (productData.name) p.name = productData.name;
        if (productData.description !== undefined) p.description = productData.description;
        if (productData.image_url) p.image_url = productData.image_url;
        if (productData.badge !== undefined) p.badge = productData.badge;
        if (productData.is_promo !== undefined) p.is_promo = productData.is_promo ? 1 : 0;
        if (productData.is_featured !== undefined) p.is_featured = productData.is_featured ? 1 : 0;
        if (productData.variants && productData.variants.length > 0) {
          p.variants = productData.variants;
          p.presentations = productData.variants.map(v => v.presentation_name);
          p.costs = productData.variants.map(v => Number(v.cost_price));
          p.prices = productData.variants.map(v => Number(v.sale_price));
          p.list_prices = productData.variants.map(v => Number(v.list_price));
        }
      }
    }
    return true;
  },

  async createProduct(productData) {
    if (!this.supabaseClient) this.init();
    let createdId = Date.now() % 1000000 + 500;

    if (this.supabaseClient) {
      try {
        const slug = productData.slug || productData.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
        const { data: maxP } = await this.supabaseClient.from('products').select('id').order('id', { ascending: false }).limit(1);
        const nextId = (maxP && maxP[0] && maxP[0].id) ? maxP[0].id + 1 : createdId;

        const prodInsert = {
          id: nextId,
          name: productData.name,
          slug: slug,
          description: productData.description || '',
          pet_type: productData.pet_type || 'ambos',
          subcat: productData.subcat || 'general',
          breed_size: productData.breed_size || 'todas',
          badge: productData.badge || (productData.is_promo ? 'OFERTA' : ''),
          image_url: productData.image_url || '',
          is_featured: Boolean(productData.is_featured),
          is_promo: Boolean(productData.is_promo),
          promo_tag: productData.promo_tag || '',
          active: true
        };

        const { data: newP } = await this.supabaseClient.from('products').insert(prodInsert).select();
        if (newP && newP[0]) {
          createdId = newP[0].id;
          if (productData.variants && productData.variants.length > 0) {
            const varInserts = productData.variants.map(v => ({
              product_id: createdId,
              presentation_name: v.presentation_name,
              weight_kg: Number(v.weight_kg || 1),
              cost_price: Number(v.cost_price || 1000),
              margin_percent: Number(v.margin_percent || 25),
              sale_price: Number(v.sale_price || 1250),
              list_price: Number(v.list_price || 1438),
              stock_qty: Number(v.stock_qty || 100),
              sku: v.sku || `MALY-${createdId}`
            }));
            await this.supabaseClient.from('product_variants').insert(varInserts);
          }
        }
      } catch (e) {}
    }

    return productData;
  },

  async getSettings() {
    if (!this.supabaseClient) this.init();

    if (this.supabaseClient) {
      try {
        const { data, error } = await this.supabaseClient.from('store_settings').select('key, value');
        if (!error && Array.isArray(data) && data.length > 0) {
          const settings = {};
          data.forEach(item => { settings[item.key] = item.value; });
          this.isSupabaseConnected = true;
          return settings;
        }
      } catch (e) {}
    }

    try {
      const res = await fetch(`${this.baseUrl}/api/settings`);
      if (res.ok) {
        this.isBackendConnected = true;
        return await res.json();
      }
    } catch (e) {}

    return null;
  },

  async updateSetting(key, value) {
    if (!this.supabaseClient) this.init();

    if (this.supabaseClient) {
      try {
        await this.supabaseClient.from('store_settings').upsert({ key: key, value: String(value) }, { onConflict: 'key' });
      } catch (e) {}
    }

    try {
      await fetch(`${this.baseUrl}/api/settings/${key}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: String(value) })
      });
    } catch (e) {}
  },

  async recordVisit(sessionId) {
    if (!this.supabaseClient) this.init();

    if (this.supabaseClient) {
      try {
        await this.supabaseClient.from('site_visits').insert({
          session_id: sessionId,
          user_agent: (typeof navigator !== 'undefined' && navigator.userAgent) ? navigator.userAgent.substring(0, 200) : ''
        });
      } catch (e) {}
    }
  },

  async getStats() {
    if (!this.supabaseClient) this.init();

    if (this.supabaseClient) {
      try {
        const { count: prodCount } = await this.supabaseClient.from('products').select('*', { count: 'exact', head: true }).eq('active', true);
        const { count: visitCount } = await this.supabaseClient.from('site_visits').select('*', { count: 'exact', head: true });
        const { data: visits } = await this.supabaseClient.from('site_visits').select('session_id, visit_date, visit_time').order('visit_time', { ascending: false }).limit(100);

        const uniqueSessions = new Set((visits || []).map(v => v.session_id)).size;
        const todayStr = new Date().toISOString().split('T')[0];
        const todayVisits = (visits || []).filter(v => v.visit_date === todayStr).length;
        const lastVisit = (visits && visits[0]) ? new Date(visits[0].visit_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Reciente';

        return {
          total_products: prodCount || 144,
          total_views: visitCount || 1,
          unique_visitors: uniqueSessions || 1,
          today_views: todayVisits || 1,
          last_visit: lastVisit
        };
      } catch (e) {}
    }

    return {
      total_products: 144,
      total_views: 1,
      unique_visitors: 1,
      today_views: 1,
      last_visit: 'Reciente'
    };
  },

  async submitOrder(orderPayload) {
    if (!this.supabaseClient) this.init();
    const orderCode = `ORD-${Date.now().toString(36).toUpperCase()}`;

    if (this.supabaseClient) {
      try {
        await this.supabaseClient.from('orders').insert({
          order_code: orderCode,
          customer_name: orderPayload.customer_name || 'Cliente Web WhatsApp',
          customer_phone: orderPayload.customer_phone || '',
          customer_address: orderPayload.customer_address || '',
          payment_method: orderPayload.payment_method || 'A convenir',
          subtotal: orderPayload.subtotal || 0,
          total: orderPayload.total || 0,
          notes: orderPayload.notes || 'Pedido desde tienda web',
          status: 'pendiente'
        });
      } catch (e) {}
    }

    return { order_code: orderCode, status: 'pendiente' };
  },

    normalizeSearchText(str) {
    if (!str) return '';
    return str
      .toString()
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .toLowerCase()
      .trim();
  },

  searchProductsLike(query, list = []) {
    if (!query || !query.trim()) return list;
    const normQ = this.normalizeSearchText(query);
    const tokens = normQ.split(/\s+/).filter(t => t.length > 0);
    if (!tokens.length) return list;

    return list.filter(p => {
      const presStr = Array.isArray(p.presentations) ? p.presentations.join(' ') : (p.presentation || '');
      const fields = [
        p.name || '',
        p.brand || p.brand_name || '',
        p.category || p.category_name || p.category_slug || '',
        p.subcat || '',
        p.pet_type || '',
        p.breed_size || '',
        p.description || '',
        presStr,
        p.promo_tag || '',
        p.badge || ''
      ];
      const searchable = this.normalizeSearchText(fields.join(' '));
      return tokens.every(token => searchable.includes(token));
    });
  },

  filterLocalProducts(params = {}) {
    const catalogSource = (typeof LOCAL_CATALOG !== 'undefined' && Array.isArray(LOCAL_CATALOG) && LOCAL_CATALOG.length) 
                          ? LOCAL_CATALOG 
                          : (typeof window !== 'undefined' && Array.isArray(window.LOCAL_CATALOG) ? window.LOCAL_CATALOG : []);
    
    if (!catalogSource || !catalogSource.length) return [];
    let list = [...catalogSource];
    
    if (params.category && params.category !== 'todos') {
      if (params.category === 'promociones') list = list.filter(p => p.is_promo || p.promo);
      else list = list.filter(p => p.category === params.category || p.category_slug === params.category);
    }
    if (params.pet_type && params.pet_type !== 'todos') {
      list = list.filter(p => p.pet_type === params.pet_type || p.pet_type === 'ambos');
    }
    if (params.subcat && params.subcat !== 'todas') {
      list = list.filter(p => p.subcat === params.subcat);
    }
    if (params.breed_size && params.breed_size !== 'todas') {
      list = list.filter(p => p.breed_size === params.breed_size || p.breed_size === 'todas');
    }
    if (params.brand && params.brand !== 'todas') {
      list = list.filter(p => (p.brand || '').toLowerCase() === params.brand.toLowerCase());
    }
    if (params.promoOnly) {
      list = list.filter(p => p.is_promo || p.promo);
    }
    if (params.search) {
      list = this.searchProductsLike(params.search, list);
    }
    return list;
  }
};

var API = window.API;

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    if (window.API) window.API.init();
  });
}
