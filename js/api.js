/**
 * MalyPetShop - Capa de Servicio API
 */
const API = {
  baseUrl: window.location.origin.includes('http') ? window.location.origin : 'http://localhost:8000',
  isBackendConnected: false,

  async checkHealth() {
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

  async getProducts(params = {}) {
    if (this.isBackendConnected) {
      try {
        const query = new URLSearchParams();
        if (params.category && params.category !== 'todos') query.append('category', params.category);
        if (params.pet_type && params.pet_type !== 'todos') query.append('pet_type', params.pet_type);
        if (params.subcat && params.subcat !== 'todas') query.append('subcat', params.subcat);
        if (params.breed_size && params.breed_size !== 'todas') query.append('breed_size', params.breed_size);
        if (params.brand && params.brand !== 'todas') query.append('brand', params.brand);
        if (params.promoOnly) query.append('is_promo', 'true');
        if (params.search) query.append('search', params.search);
        if (params.margin_policy) query.append('margin_policy', params.margin_policy);

        const res = await fetch(`${this.baseUrl}/api/products?${query.toString()}`);
        if (res.ok) return await res.json();
      } catch (err) {
        console.error("Error al consultar API de productos, usando fallback local:", err);
      }
    }
    return this.filterLocalProducts(params);
  },

  async createProduct(productData) {
    let createdItem = null;
    if (this.isBackendConnected) {
      try {
        const res = await fetch(`${this.baseUrl}/api/products`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(productData)
        });
        if (res.ok) {
          createdItem = await res.json();
        }
      } catch (e) {
        console.warn('Fallo guardando en backend, se guardará en almacenamiento local:', e);
      }
    }

    // Adaptación a formato de catálogo en memoria y localStorage
    const newId = (createdItem && createdItem.id) ? createdItem.id : (Date.now() % 1000000 + 500);
    const variants = productData.variants || [];
    const presentations = variants.map(v => v.presentation_name);
    const costs = variants.map(v => Number(v.cost_price));
    const prices = variants.map(v => Number(v.sale_price || Math.round(v.cost_price * (1 + (v.margin_percent || 25) / 100))));
    const list_prices = variants.map(v => Number(v.list_price || Math.round(prices[0] * 1.15)));

    const localItem = {
      id: newId,
      name: productData.name,
      slug: productData.slug || productData.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
      description: productData.description || '',
      desc: productData.description || '',
      pet_type: productData.pet_type || 'ambos',
      subcat: productData.subcat || 'general',
      breed_size: productData.breed_size || 'todas',
      badge: productData.badge || (productData.is_promo ? 'OFERTA' : ''),
      image_url: productData.image_url || 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80',
      is_featured: !!productData.is_featured,
      featured: !!productData.is_featured,
      is_promo: !!productData.is_promo,
      promo: !!productData.is_promo,
      promo_tag: productData.promo_tag || '',
      category_name: productData.category || 'General',
      category_slug: productData.category || 'perros',
      category: productData.category || 'perros',
      brand_name: productData.brand || 'General',
      brand: productData.brand || 'General',
      variants: variants,
      presentations: presentations,
      costs: costs,
      prices: prices,
      list_prices: list_prices
    };

    // Añadir a LOCAL_CATALOG si no está
    const exists = LOCAL_CATALOG.find(p => p.id === localItem.id || p.slug === localItem.slug);
    if (!exists) {
      LOCAL_CATALOG.unshift(localItem);
    }

    // Persistir en localStorage
    const manualProds = JSON.parse(localStorage.getItem('petshop_manual_products') || '[]');
    manualProds.unshift(localItem);
    localStorage.setItem('petshop_manual_products', JSON.stringify(manualProds));

    return localItem;
  },

  async updateProduct(productId, productData) {
    if (this.isBackendConnected) {
      try {
        await fetch(`${this.baseUrl}/api/products/${productId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(productData)
        });
      } catch (e) {
        console.warn("Fallo actualizando producto en backend:", e);
      }
    }

    // Actualizar en LOCAL_CATALOG
    const pIndex = LOCAL_CATALOG.findIndex(p => p.id === productId);
    if (pIndex > -1) {
      const p = LOCAL_CATALOG[pIndex];
      if (productData.name) p.name = productData.name;
      if (productData.description !== undefined) {
        p.description = productData.description;
        p.desc = productData.description;
      }
      if (productData.brand) {
        p.brand = productData.brand;
        p.brand_name = productData.brand;
      }
      if (productData.category) {
        p.category = productData.category;
        p.category_slug = productData.category;
      }
      if (productData.pet_type) p.pet_type = productData.pet_type;
      if (productData.subcat) p.subcat = productData.subcat;
      if (productData.breed_size) p.breed_size = productData.breed_size;
      if (productData.badge !== undefined) p.badge = productData.badge;
      if (productData.image_url) p.image_url = productData.image_url;
      if (productData.is_featured !== undefined) {
        p.is_featured = productData.is_featured ? 1 : 0;
        p.featured = Boolean(productData.is_featured);
      }
      if (productData.is_promo !== undefined) {
        p.is_promo = productData.is_promo ? 1 : 0;
        p.promo = Boolean(productData.is_promo);
      }
      if (productData.promo_tag !== undefined) p.promo_tag = productData.promo_tag;

      if (productData.variants && productData.variants.length > 0) {
        p.variants = productData.variants;
        p.presentations = productData.variants.map(v => v.presentation_name);
        p.costs = productData.variants.map(v => Number(v.cost_price));
        p.prices = productData.variants.map(v => Number(v.sale_price));
        p.list_prices = productData.variants.map(v => Number(v.list_price));
      }
    }

    // Actualizar en localStorage si existe en manual products
    const manualProds = JSON.parse(localStorage.getItem('petshop_manual_products') || '[]');
    const mIdx = manualProds.findIndex(p => p.id === productId);
    if (mIdx > -1) {
      manualProds[mIdx] = { ...manualProds[mIdx], ...productData };
      localStorage.setItem('petshop_manual_products', JSON.stringify(manualProds));
    }

    // Guardar si cambió la imagen en custom images
    if (productData.image_url) {
      const custom = JSON.parse(localStorage.getItem('petshop_custom_images') || '{}');
      custom[productId] = productData.image_url;
      localStorage.setItem('petshop_custom_images', JSON.stringify(custom));
    }

    return true;
  },

  async updateProductImage(productId, imageUrl) {
    // 1. Guardar en SQLite vía API si está conectado
    if (this.isBackendConnected) {
      try {
        await fetch(`${this.baseUrl}/api/products/${productId}/image`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_url: imageUrl })
        });
      } catch (e) {
        console.warn("No se pudo persistir en backend, guardando localmente:", e);
      }
    }
    // 2. Guardar en localStorage para respaldo permanente en cualquier entorno
    const custom = JSON.parse(localStorage.getItem('petshop_custom_images') || '{}');
    custom[productId] = imageUrl;
    localStorage.setItem('petshop_custom_images', JSON.stringify(custom));
    return true;
  },

  async getSettings() {
    try {
      const res = await fetch(`${this.baseUrl}/api/settings`);
      if (res.ok) {
        this.isBackendConnected = true;
        return await res.json();
      }
    } catch (e) {
      // Backend local desconectado
    }
    return null;
  },

  async updateSetting(key, value) {
    try {
      await fetch(`${this.baseUrl}/api/settings/${key}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: String(value) })
      });
      this.isBackendConnected = true;
    } catch (e) {
      console.warn("Fallo guardando setting en backend:", e);
    }
  },

  async recordVisit(sessionId) {
    try {
      await fetch(`${this.baseUrl}/api/analytics/visit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
      });
    } catch (e) {
      // Offline local mode
    }
  },

  async getStats() {
    if (this.isBackendConnected) {
      try {
        const res = await fetch(`${this.baseUrl}/api/stats`);
        if (res.ok) return await res.json();
      } catch (e) {}
    }
    return {
      total_products: LOCAL_CATALOG.length,
      total_variants: LOCAL_CATALOG.reduce((acc, p) => acc + (p.variants ? p.variants.length : p.presentations.length), 0),
      total_brands: 30,
      total_categories: 6,
      total_orders: JSON.parse(localStorage.getItem('petshop_orders') || '[]').length
    };
  },

  async submitOrder(orderData) {
    if (this.isBackendConnected) {
      try {
        const res = await fetch(`${this.baseUrl}/api/orders`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(orderData)
        });
        if (res.ok) return await res.json();
      } catch (e) {}
    }
    const orders = JSON.parse(localStorage.getItem('petshop_orders') || '[]');
    const localOrder = {
      order_id: Date.now(),
      order_code: `ORD-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
      created_at: new Date().toISOString(),
      ...orderData
    };
    orders.push(localOrder);
    localStorage.setItem('petshop_orders', JSON.stringify(orders));
    return localOrder;
  },

  filterLocalProducts(params = {}) {
    // Cargar productos creados manualmente en localStorage si no están en LOCAL_CATALOG
    const manualProds = JSON.parse(localStorage.getItem('petshop_manual_products') || '[]');
    manualProds.forEach(mp => {
      if (!LOCAL_CATALOG.some(p => p.id === mp.id || p.slug === mp.slug)) {
        LOCAL_CATALOG.unshift(mp);
      }
    });

    let list = [...LOCAL_CATALOG];
    const margin = params.margin_policy || localStorage.getItem('petshop_margin_policy') || 'recommended';
    const customImages = JSON.parse(localStorage.getItem('petshop_custom_images') || '{}');

    // Aplicar imágenes personalizadas si existen
    list = list.map(p => {
      const copy = { ...p };
      if (customImages[p.id]) {
        copy.image_url = customImages[p.id];
      }
      if (margin !== 'recommended') {
        const pct = parseFloat(margin) / 100.0;
        copy.prices = copy.costs.map(c => Math.round(c * (1.0 + pct)));
        copy.list_prices = copy.prices.map(pr => Math.round(pr * 1.15));
      }
      return copy;
    });

    if (params.category && params.category !== 'todos') {
      if (params.category === 'promociones') {
        list = list.filter(p => p.is_promo || p.promo);
      } else {
        list = list.filter(p => p.category_slug === params.category || p.category === params.category);
      }
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
      list = list.filter(p => (p.brand_name || p.brand) === params.brand);
    }
    if (params.promoOnly) {
      list = list.filter(p => p.is_promo || p.promo);
    }
    if (params.search) {
      const q = params.search.toLowerCase().trim();
      list = list.filter(p => 
        p.name.toLowerCase().includes(q) || 
        (p.brand_name || p.brand || '').toLowerCase().includes(q) || 
        (p.description || p.desc || '').toLowerCase().includes(q)
      );
    }
    return list;
  }
};
