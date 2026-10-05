
// -------------------------------------------------------------
// MODAL DE DETALLE DE PRODUCTO Y ZOOM INTERACTIVO
// -------------------------------------------------------------
let currentDetailProduct = null;
let currentDetailPresIdx = 0;
let currentDetailQty = 1;

function handleProductCardClick(event, productId) {
  // Ignorar clicks en selector de presentación, agregar a bolsa o WhatsApp directo
  if (event.target.closest('.pres-pill') || event.target.closest('.btn-add-cart') || event.target.closest('.btn-wa-card')) {
    return;
  }
  openProductDetailModal(productId);
}

function openProductDetailModal(productId) {
  const p = PRODUCTS_DB.find(item => item.id === productId);
  if (!p) return;

  currentDetailProduct = p;
  currentDetailPresIdx = selectedPresIndices[p.id] !== undefined ? selectedPresIndices[p.id] : 0;
  if (currentDetailPresIdx >= (p.presentations || []).length) currentDetailPresIdx = 0;
  currentDetailQty = 1;

  renderProductDetailModal();
  const modal = document.getElementById('productDetailModal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function closeProductDetailModal() {
  const modal = document.getElementById('productDetailModal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

function closeProductDetailModalOnBackdrop(event) {
  if (event.target.id === 'productDetailModal') {
    closeProductDetailModal();
  }
}

function renderProductDetailModal() {
  const p = currentDetailProduct;
  if (!p) return;

  const presList = p.presentations || ["Única"];
  const brandName = p.brand_name || p.brand || "Premium";
  const catName = p.category_name || p.category || "General";
  const badgeText = p.badge || (p.is_promo ? (p.promo_tag || "Oferta Especial") : "");

  const pillsHTML = presList.map((pres, idx) => `
    <button type="button" class="detail-pres-pill ${idx === currentDetailPresIdx ? 'active' : ''}"
            onclick="selectDetailPresentation(${idx})">
      ${pres}
    </button>
  `).join('');

  const safeName = (p.name || '').replace(/'/g, "\\'");
  const safeImg = p.image_url || '';

  const content = document.getElementById('productDetailContent');
  if (!content) return;

  content.innerHTML = `
    <!-- Columna Izquierda: Imagen y Zoom -->
    <div class="detail-image-container">
      <div class="detail-zoom-wrapper" id="detailZoomWrapper" 
           onmousemove="handleImageZoom(event)" 
           onmouseleave="resetImageZoom(event)"
           onclick="openLightboxZoom('${safeImg}', '${safeName}')">
        <img class="detail-zoom-img" referrerpolicy="no-referrer" id="detailZoomImg" src="${safeImg}" alt="${p.name}"
             onerror="this.src='https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80'">
      </div>
      <div class="zoom-instruction-badge" onclick="openLightboxZoom('${safeImg}', '${safeName}')">
        <span>🔍</span> Pasá el cursor para lupa | Clic para pantalla completa
      </div>
    </div>

    <!-- Columna Derecha: Información del Producto -->
    <div class="detail-info-col">
      <div class="detail-badges-row">
        <span class="detail-badge brand">${brandName}</span>
        <span class="detail-badge cat">${catName}</span>
        ${badgeText ? `<span class="detail-badge promo">${badgeText}</span>` : ''}
      </div>

      <h2 class="detail-title">${p.name}</h2>

      <p class="detail-desc">${p.description || p.desc || 'Producto original con garantía de fábrica y envasado hermético.'}</p>

      <div class="detail-pres-section">
        <label>Presentación seleccionada:</label>
        <div class="detail-pres-pills">
          ${pillsHTML}
        </div>
      </div>

      <!-- Cuadro de Precio con Total Dinámico según Cantidad -->
      <div class="detail-price-box">
        <div>
          <div style="font-size: 0.78rem; color: #64748b; font-weight: 700; text-transform: uppercase;">Importe Total:</div>
          <div style="display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;">
            <span class="detail-price-list" id="detailPriceList"></span>
            <span class="detail-price-main" id="detailPriceMain"></span>
          </div>
          <div id="detailPriceSubcalc" style="margin-top: 3px;"></div>
        </div>
        <span class="discount-chip" id="detailDiscountChip" style="display: none;"></span>
      </div>

      <!-- Selector de Cantidad y Botones de Acción -->
      <div class="detail-qty-actions">
        <div class="detail-qty-selector">
          <button type="button" class="detail-qty-btn" onclick="updateDetailQty(-1)" title="Restar 1">−</button>
          <input type="text" class="detail-qty-input" id="detailQtyInput" value="${currentDetailQty}" readonly>
          <button type="button" class="detail-qty-btn" onclick="updateDetailQty(1)" title="Sumar 1">+</button>
        </div>

        <button type="button" class="btn-detail-add" id="btnDetailAdd" onclick="addDetailToCart()">
          <span>🛒</span> <span id="btnDetailAddText">Agregar a la Bolsa</span>
        </button>

        <button type="button" class="btn-detail-wa" onclick="askDetailWhatsApp()">
          <span>💬</span> Consultar WhatsApp
        </button>
      </div>

      <div style="font-size: 0.8rem; color: #64748b; line-height: 1.5; margin-top: 10px; background: #f8fafc; padding: 10px 14px; border-radius: 8px; border: 1px solid #e2e8f0;">
        🚚 <strong>Envío a domicilio coordinado:</strong> Confirmamos stock y coordinamos entrega rápida por WhatsApp para Ciudad Evita y alrededores.
      </div>
    </div>
  `;

  updateDetailPriceDisplay();
}

function updateDetailPriceDisplay() {
  const p = currentDetailProduct;
  if (!p) return;

  const pricesList = p.prices || [0];
  const listPricesList = p.list_prices || pricesList.map(pr => Math.round(pr * 1.15));

  const unitPrice = pricesList[currentDetailPresIdx] || 0;
  const unitListPrice = listPricesList[currentDetailPresIdx] || Math.round(unitPrice * 1.15);

  const totalPrice = unitPrice * currentDetailQty;
  const totalListPrice = unitListPrice * currentDetailQty;
  const isPromo = Boolean(p.is_promo || p.promo);

  const input = document.getElementById('detailQtyInput');
  if (input) input.value = currentDetailQty;

  const mainPriceEl = document.getElementById('detailPriceMain');
  if (mainPriceEl) {
    mainPriceEl.textContent = `$${totalPrice.toLocaleString('es-AR')}`;
  }

  const listPriceEl = document.getElementById('detailPriceList');
  if (listPriceEl) {
    if (isPromo) {
      listPriceEl.textContent = `$${totalListPrice.toLocaleString('es-AR')}`;
      listPriceEl.style.display = 'inline';
    } else {
      listPriceEl.style.display = 'none';
    }
  }

  const chipEl = document.getElementById('detailDiscountChip');
  if (chipEl) {
    if (isPromo) {
      const discountPct = Math.round((1 - unitPrice / unitListPrice) * 100);
      const savings = totalListPrice - totalPrice;
      chipEl.textContent = savings > 0 ? `AHORRÁS $${savings.toLocaleString('es-AR')} (${discountPct}%)` : 'PRECIO ESPECIAL';
      chipEl.style.display = 'inline-block';
    } else {
      chipEl.style.display = 'none';
    }
  }

  const subcalcEl = document.getElementById('detailPriceSubcalc');
  if (subcalcEl) {
    if (currentDetailQty > 1) {
      subcalcEl.innerHTML = `<span style="color: #64748b; font-size: 0.82rem; font-weight: 600;">($${unitPrice.toLocaleString('es-AR')} c/u • ${currentDetailQty} unidades)</span>`;
    } else {
      subcalcEl.innerHTML = '';
    }
  }

  const btnAddText = document.getElementById('btnDetailAddText');
  if (btnAddText) {
    const qtyText = currentDetailQty > 1 ? ` (${currentDetailQty})` : '';
    btnAddText.textContent = `Agregar${qtyText} a la Bolsa • $${totalPrice.toLocaleString('es-AR')}`;
  }
}

function selectDetailPresentation(idx) {
  currentDetailPresIdx = idx;
  if (currentDetailProduct) {
    selectedPresIndices[currentDetailProduct.id] = idx;
    selectPresentation(currentDetailProduct.id, idx);
  }
  document.querySelectorAll('.detail-pres-pill').forEach((pill, i) => {
    pill.classList.toggle('active', i === idx);
  });
  updateDetailPriceDisplay();
}

function updateDetailQty(delta) {
  currentDetailQty = Math.max(1, currentDetailQty + delta);
  updateDetailPriceDisplay();
}

function addDetailToCart() {
  if (!currentDetailProduct) return;
  const p = currentDetailProduct;
  const pres = (p.presentations && p.presentations[currentDetailPresIdx]) || "Única";
  const unitPrice = (p.prices && p.prices[currentDetailPresIdx]) || 0;

  // Usar el array global cart (en minúscula)
  const existingIndex = cart.findIndex(item => item.id === p.id && item.presentation === pres);
  if (existingIndex > -1) {
    cart[existingIndex].quantity += currentDetailQty;
  } else {
    cart.push({
      id: p.id,
      name: p.name,
      brand: p.brand_name || p.brand || "",
      presentation: pres,
      price: unitPrice,
      quantity: currentDetailQty,
      image: p.image_url
    });
  }

  saveCart();
  updateCartBadge();
  renderCartDrawer();
  openCartDrawer();
  closeProductDetailModal();
}

function askDetailWhatsApp() {
  if (!currentDetailProduct) return;
  const p = currentDetailProduct;
  const pres = (p.presentations && p.presentations[currentDetailPresIdx]) || "Única";
  const unitPrice = (p.prices && p.prices[currentDetailPresIdx]) || 0;
  const totalPrice = unitPrice * currentDetailQty;

  let msg = `Hola ${CONFIG.storeName}! Quisiera consultar por el siguiente producto:

`;
  msg += `*${p.name}*
`;
  msg += `Presentación: ${pres}
`;
  msg += `Cantidad: ${currentDetailQty} unidad${currentDetailQty > 1 ? 'es' : ''}
`;
  msg += `Precio unitario: $${unitPrice.toLocaleString('es-AR')}
`;
  if (currentDetailQty > 1) {
    msg += `Total (${currentDetailQty} u.): $${totalPrice.toLocaleString('es-AR')}
`;
  }
  msg += `
¿Tienen stock y podemos coordinar la entrega?`;

  const waUrl = `https://wa.me/${CONFIG.waNumber}?text=${encodeURIComponent(msg)}`;
  window.open(waUrl, '_blank');
}

// ZOOM INTERACTIVO DE LUPA
function handleImageZoom(event) {
  const wrapper = document.getElementById('detailZoomWrapper');
  const img = document.getElementById('detailZoomImg');
  if (!wrapper || !img) return;

  const rect = wrapper.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  const xPercent = Math.max(0, Math.min(100, (x / rect.width) * 100));
  const yPercent = Math.max(0, Math.min(100, (y / rect.height) * 100));

  img.style.transformOrigin = `${xPercent}% ${yPercent}%`;
  img.style.transform = 'scale(2.3)';
}

function resetImageZoom() {
  const img = document.getElementById('detailZoomImg');
  if (!img) return;
  img.style.transform = 'scale(1)';
  img.style.transformOrigin = 'center center';
}

// LIGHTBOX FULLSCREEN ZOOM
function openLightboxZoom(imgUrl, caption) {
  const modal = document.getElementById('imageLightboxModal');
  const img = document.getElementById('lightboxImg');
  const cap = document.getElementById('lightboxCaption');
  if (!modal || !img) return;

  img.src = imgUrl;
  if (cap) cap.textContent = caption || '';
  modal.style.display = 'flex';
}

function closeImageLightbox(event) {
  if (event && event.target && event.target.id === 'lightboxImg') return;
  const modal = document.getElementById('imageLightboxModal');
  if (modal) modal.style.display = 'none';
}

/**
 * MalyPetShop - Controlador Principal
 * Solución definitiva de selección múltiple, gestión de imágenes desde admin y promociones seleccionadas.
 */

function getInstagramUrl(userOrUrl) {
  if (!userOrUrl) return 'https://instagram.com/maly.petshop';
  const val = userOrUrl.trim();
  if (val.startsWith('http://') || val.startsWith('https://')) {
    return val;
  }
  const cleanUser = val.replace(/^@+/, '').trim();
  return `https://instagram.com/${cleanUser}`;
}

function trackSiteVisit() {
  const todayStr = new Date().toISOString().slice(0, 10);
  const nowTimeStr = new Date().toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  let sessionId = sessionStorage.getItem('maly_session_id');
  if (!sessionId) {
    sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);
    sessionStorage.setItem('maly_session_id', sessionId);
  }

  try {
    let localStats = JSON.parse(localStorage.getItem('maly_analytics') || '{}');
    localStats.total_views = (localStats.total_views || 0) + 1;
    if (!localStats.sessions) localStats.sessions = [];
    if (!localStats.sessions.includes(sessionId)) {
      localStats.sessions.push(sessionId);
    }
    if (localStats.current_date !== todayStr) {
      localStats.current_date = todayStr;
      localStats.today_views = 0;
    }
    localStats.today_views = (localStats.today_views || 0) + 1;
    localStats.last_visit = nowTimeStr;
    localStorage.setItem('maly_analytics', JSON.stringify(localStats));
  } catch (e) {}

  API.recordVisit(sessionId);
}

function goToInstagram(event) {
  if (event) event.preventDefault();
  const inputEl = document.getElementById('inputInstagram');
  const freshIg = (inputEl && inputEl.value.trim()) || CONFIG.instagram || localStorage.getItem('petshop_ig') || 'maly.petshop';
  const url = getInstagramUrl(freshIg);
  window.open(url, '_blank');
}

let PRODUCTS_DB = [];
let selectedPresIndices = {};
let cart = JSON.parse(localStorage.getItem('petshop_cart') || '[]');

let CONFIG = {
  storeName: localStorage.getItem('petshop_name') || "Maly Petshop",
  waNumber: localStorage.getItem('petshop_wa') || "5491158549783",
  instagram: localStorage.getItem('petshop_ig') || "maly.petshop",
  marginPolicy: localStorage.getItem('petshop_margin_policy') || "recommended",
  adminPin: localStorage.getItem('petshop_admin_pin') || "1234"
};

let currentSlide = 0;
let carouselInterval = null;
const TOTAL_SLIDES = 3;

let catalogFilters = {
  category: 'todos',
  subcat: 'todas',
  breed_size: 'todas',
  promoOnly: false,
  search: ''
};

// INICIALIZACIÓN
document.addEventListener('DOMContentLoaded', async () => {
  // Registrar ingreso de visitante en el monitor de estadísticas
  trackSiteVisit();
  // Asegurar apertura de menús desplegables con clic además de hover
  document.querySelectorAll('.nav-item').forEach(item => {
    const menu = item.querySelector('.dropdown-menu');
    if (menu) {
      item.addEventListener('click', (e) => {
        if (e.target.closest('.dropdown-item')) return;
        document.querySelectorAll('.nav-item').forEach(other => {
          if (other !== item) other.classList.remove('open');
        });
        item.classList.toggle('open');
      });
    }
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-item')) {
      document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('open'));
    }
  });
  // 1. Aplicar de inmediato el nombre de la tienda desde localStorage
  applyConfigToDOM();

  // 2. Sincronizar configuraciones con el backend SQLite
  try {
    const remoteSettings = await API.getSettings();
    if (remoteSettings) {
      if (remoteSettings.store_name) {
        CONFIG.storeName = remoteSettings.store_name;
        localStorage.setItem('petshop_name', CONFIG.storeName);
      }
      if (remoteSettings.whatsapp_number) {
        CONFIG.waNumber = remoteSettings.whatsapp_number;
        localStorage.setItem('petshop_wa', CONFIG.waNumber);
      }
      if (remoteSettings.instagram_user) {
        CONFIG.instagram = remoteSettings.instagram_user;
        localStorage.setItem('petshop_ig', CONFIG.instagram);
      }
      if (remoteSettings.admin_pin) {
        CONFIG.adminPin = remoteSettings.admin_pin;
        localStorage.setItem('petshop_admin_pin', CONFIG.adminPin);
      }
      if (remoteSettings.margin_policy) {
        CONFIG.marginPolicy = remoteSettings.margin_policy;
        localStorage.setItem('petshop_margin_policy', CONFIG.marginPolicy);
      }
      applyConfigToDOM();
    }
  } catch (e) {
    console.warn("No se pudieron cargar settings del backend:", e);
  }

  initCarousel();
  await loadCatalogAndRender();
  updateCartBadge();
  setupEventListeners();
  checkDbStatus();

  // Atajo de teclado para acceder al panel de administración: Ctrl + Shift + A
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === 'A' || e.key === 'a')) {
      e.preventDefault();
      openSettingsModal();
    }
  });

  if (window.location.hash === '#admin') {
    openSettingsModal();
  }
});

async function checkDbStatus() {
  const health = await API.checkHealth();
  const badge = document.getElementById('dbStatusIndicator');
  if (!badge) return;
  if (health) {
    badge.className = 'db-status-badge online';
    badge.innerHTML = `🟢 Conectado a SQLite REST API (${health.active_products} productos cargados)`;
  } else {
    badge.className = 'db-status-badge local';
    badge.innerHTML = `🟡 Modo Autónomo Local (Catálogo completo de 89 productos)`;
  }
}

async function loadCatalogAndRender() {
  showLoading(true);
  try {
    PRODUCTS_DB = await API.getProducts({
      margin_policy: CONFIG.marginPolicy,
      ...catalogFilters
    });

    // Cargar fotos personalizadas desde localStorage si existen
    const customImages = JSON.parse(localStorage.getItem('petshop_custom_images') || '{}');
    PRODUCTS_DB.forEach(p => {
      if (customImages[p.id]) {
        p.image_url = customImages[p.id];
      }
      if (selectedPresIndices[p.id] === undefined) {
        selectedPresIndices[p.id] = (p.presentations && p.presentations.length > 0) ? p.presentations.length - 1 : 0;
      }
    });

    renderHomepageGrids();
    renderCatalogGrid();
  } catch (err) {
    console.error("Error al cargar catálogo:", err);
  } finally {
    showLoading(false);
  }
}

function showLoading(show) {
  const loaders = document.querySelectorAll('.grid-loader');
  loaders.forEach(l => l.style.display = show ? 'block' : 'none');
}

function renderHomepageGrids() {
  const featuredGrid = document.getElementById('featuredGrid');
  const promosGrid = document.getElementById('promosGrid');
  const snacksGrid = document.getElementById('snacksGrid');

  if (featuredGrid) {
    const featured = PRODUCTS_DB.filter(p => p.is_featured || p.featured).slice(0, 8);
    featuredGrid.innerHTML = featured.map(p => createProductCardHTML(p)).join('');
  }

  if (promosGrid) {
    const promos = PRODUCTS_DB.filter(p => p.is_promo || p.promo).slice(0, 8);
    promosGrid.innerHTML = promos.map(p => createProductCardHTML(p)).join('');
  }

  if (snacksGrid) {
    const snacks = PRODUCTS_DB.filter(p => p.category_slug === 'snacks' || p.category === 'snacks' || p.subcat === 'snacks').slice(0, 8);
    snacksGrid.innerHTML = snacks.map(p => createProductCardHTML(p)).join('');
  }
}

function renderCatalogGrid() {
  const catalogGrid = document.getElementById('catalogGrid');
  if (!catalogGrid) return;

  const countBadge = document.getElementById('catalogCountBadge');
  if (countBadge) countBadge.textContent = `${PRODUCTS_DB.length} productos disponibles`;

  if (PRODUCTS_DB.length === 0) {
    catalogGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 50px 20px; background: white; border-radius: 16px; border: 1px dashed #cbd5e1;">
        <span style="font-size: 2.5rem; display: block; margin-bottom: 10px;">🔍</span>
        <h3 style="font-size: 1.2rem; color: #1e293b; font-weight: 700;">No encontramos productos con esos filtros</h3>
        <p style="color: #64748b; font-size: 0.9rem; margin-top: 6px;">Probá seleccionando otra categoría o limpiando la búsqueda.</p>
        <button onclick="resetFilters()" style="margin-top: 14px; background: #0284c7; color: white; border: none; padding: 8px 18px; border-radius: 9999px; font-weight: 600; cursor: pointer;">Ver Todo el Catálogo</button>
      </div>
    `;
    return;
  }

  catalogGrid.innerHTML = PRODUCTS_DB.map(p => createProductCardHTML(p)).join('');
}

// -------------------------------------------------------------
// CREACIÓN DE TARJETA CON SOPORTE PARA SINCRONIZACIÓN MULTI-GRILLA
// -------------------------------------------------------------
function createProductCardHTML(p) {
  const presList = p.presentations || [];
  const pricesList = p.prices || [];
  const listPricesList = p.list_prices || pricesList.map(pr => Math.round(pr * 1.15));
  
  let currentIdx = selectedPresIndices[p.id] !== undefined ? selectedPresIndices[p.id] : 0;
  if (currentIdx >= presList.length) currentIdx = 0;

  const currentPres = presList[currentIdx] || "Única";
  const currentPrice = pricesList[currentIdx] || 0;
  const currentList = listPricesList[currentIdx] || Math.round(currentPrice * 1.15);
  const brandName = p.brand_name || p.brand || "Premium";
  const badgeText = p.badge || (p.is_promo ? (p.promo_tag || "Oferta Especial") : "");

  const pillsHTML = presList.map((pres, idx) => `
    <button type="button" class="pres-pill ${idx === currentIdx ? 'active' : ''}" 
            onclick="selectPresentation(${p.id}, ${idx})">
      ${pres}
    </button>
  `).join('');

  // Precio especial fantasma: solo para los productos más vendidos seleccionados
  let priceBlockHTML = '';
  if (p.is_promo || p.promo) {
    priceBlockHTML = `
      <div class="price-row" style="align-items: center; margin-bottom: 12px;">
        <div>
          <span class="price-list">$${currentList.toLocaleString('es-AR')}</span>
          <span class="price-main">$${currentPrice.toLocaleString('es-AR')}</span>
        </div>
        <span class="discount-chip">PRECIO ESPECIAL</span>
      </div>
    `;
  } else {
    priceBlockHTML = `
      <div class="price-row" style="align-items: center; margin-bottom: 12px;">
        <div>
          <span class="price-main">$${currentPrice.toLocaleString('es-AR')}</span>
        </div>
      </div>
    `;
  }

  return `
    <article class="product-card" data-product-id="${p.id}" onclick="handleProductCardClick(event, ${p.id})">
      <div class="card-top">
        ${badgeText ? `<span class="card-badge-top">${badgeText}</span>` : ''}
        ${p.is_promo ? `<span class="card-badge-promo">OFERTA</span>` : ''}
        
        <img class="card-img" referrerpolicy="no-referrer" src="${p.image_url}" alt="${p.name}" loading="lazy"
             onerror="this.src='https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80'">
      </div>
      <div class="card-body">
        <span class="card-brand">${brandName}</span>
        <h3 class="card-title">${p.name}</h3>
        <p class="card-desc">${p.description || p.desc || ''}</p>

        <div class="card-presentations">
          <span class="pres-label">Presentación seleccionada:</span>
          <div class="pres-pills">
            ${pillsHTML}
          </div>
        </div>

        <div class="card-pricing">
          ${priceBlockHTML}

          <div class="card-actions">
            <button class="btn-add-cart" onclick="addToCart(${p.id})">
              <span>🛒</span> Agregar a la Bolsa
            </button>
            <button class="btn-wa-card" title="Consultar por WhatsApp" onclick="askProductWhatsApp(${p.id})">
              💬
            </button>
          </div>
        </div>
      </div>
    </article>
  `;
}

// -------------------------------------------------------------
// SELECCIÓN DE PRESENTACIÓN SINCRONIZADA EN TODAS LAS GRILLAS
// -------------------------------------------------------------
function selectPresentation(productId, presIdx) {
  selectedPresIndices[productId] = presIdx;
  const p = PRODUCTS_DB.find(item => item.id === productId);
  if (!p) return;

  const price = (p.prices && p.prices[presIdx] !== undefined) ? p.prices[presIdx] : 0;
  const listPrice = (p.list_prices && p.list_prices[presIdx] !== undefined) ? p.list_prices[presIdx] : Math.round(price * 1.15);

  // Seleccionar y actualizar simultáneamente TODAS las tarjetas de este producto en la página
  const matchingCards = document.querySelectorAll(`.product-card[data-product-id="${productId}"]`);
  matchingCards.forEach(card => {
    // Actualizar pills activas
    const pills = card.querySelectorAll('.pres-pill');
    pills.forEach((pill, idx) => {
      pill.classList.toggle('active', idx === presIdx);
    });

    // Actualizar precio principal
    const priceMainEl = card.querySelector('.price-main');
    if (priceMainEl) {
      priceMainEl.textContent = `$${price.toLocaleString('es-AR')}`;
    }

    // Actualizar precio de lista tachado si corresponde
    const priceListEl = card.querySelector('.price-list');
    if (priceListEl) {
      priceListEl.textContent = `$${listPrice.toLocaleString('es-AR')}`;
    }
  });
}

// -------------------------------------------------------------
// CARRUSEL AUTOMÁTICO
// -------------------------------------------------------------
function initCarousel() {
  const track = document.getElementById('carouselTrack');
  const prevBtn = document.getElementById('prevSlideBtn');
  const nextBtn = document.getElementById('nextSlideBtn');
  const dots = document.querySelectorAll('.carousel-dot');
  const wrapper = document.querySelector('.carousel-wrapper');

  if (!track) return;

  function updateSlide() {
    track.style.transform = `translateX(-${currentSlide * 100}%)`;
    dots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === currentSlide);
    });
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % TOTAL_SLIDES;
    updateSlide();
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + TOTAL_SLIDES) % TOTAL_SLIDES;
    updateSlide();
  }

  if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); resetTimer(); });
  if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); resetTimer(); });

  dots.forEach((dot, idx) => {
    dot.addEventListener('click', () => {
      currentSlide = idx;
      updateSlide();
      resetTimer();
    });
  });

  function startTimer() {
    if (carouselInterval) clearInterval(carouselInterval);
    carouselInterval = setInterval(nextSlide, 4500);
  }

  function resetTimer() {
    clearInterval(carouselInterval);
    startTimer();
  }

  if (wrapper) {
    wrapper.addEventListener('mouseenter', () => clearInterval(carouselInterval));
    wrapper.addEventListener('mouseleave', () => startTimer());
  }

  startTimer();
  updateSlide();
}

// -------------------------------------------------------------
// CARRITO Y WHATSAPP
// -------------------------------------------------------------
function addToCart(productId) {
  const p = PRODUCTS_DB.find(item => item.id === productId);
  if (!p) return;

  const presIdx = selectedPresIndices[productId] || 0;
  const presentationName = (p.presentations && p.presentations[presIdx]) ? p.presentations[presIdx] : "Única";
  const price = (p.prices && p.prices[presIdx]) ? p.prices[presIdx] : 0;

  const existingIndex = cart.findIndex(item => item.id === productId && item.presentation === presentationName);
  if (existingIndex > -1) {
    cart[existingIndex].quantity += 1;
  } else {
    cart.push({
      id: productId,
      name: p.name,
      brand: p.brand_name || p.brand || "",
      presentation: presentationName,
      price: price,
      quantity: 1,
      image: p.image_url
    });
  }

  saveCart();
  updateCartBadge();
  renderCartDrawer();
  openCartDrawer();
}

function saveCart() {
  localStorage.setItem('petshop_cart', JSON.stringify(cart));
}

function updateCartBadge() {
  const totalItems = cart.reduce((acc, item) => acc + item.quantity, 0);
  const badge = document.getElementById('cartBadge');
  if (badge) badge.textContent = totalItems;
}

function openCartDrawer() {
  renderCartDrawer();
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('cartOverlay');
  if (drawer) drawer.classList.add('open');
  if (overlay) overlay.classList.add('open');
}

function closeCartDrawer() {
  const drawer = document.getElementById('cartDrawer');
  const overlay = document.getElementById('cartOverlay');
  if (drawer) drawer.classList.remove('open');
  if (overlay) overlay.classList.remove('open');
}

function changeCartQty(index, delta) {
  if (!cart[index]) return;
  cart[index].quantity += delta;
  if (cart[index].quantity <= 0) {
    cart.splice(index, 1);
  }
  saveCart();
  updateCartBadge();
  renderCartDrawer();
}

function removeCartItem(index) {
  cart.splice(index, 1);
  saveCart();
  updateCartBadge();
  renderCartDrawer();
}

function renderCartDrawer() {
  const body = document.getElementById('cartItemsList');
  const totalEl = document.getElementById('cartTotal');

  if (!body) return;

  if (cart.length === 0) {
    body.innerHTML = `
      <div style="text-align: center; padding: 60px 20px; color: #64748b;">
        <span style="font-size: 3rem; display: block; margin-bottom: 14px;">🛒</span>
        <h4 style="font-size: 1.1rem; color: #1e293b; font-weight: 700;">Tu bolsa de compras está vacía</h4>
        <p style="font-size: 0.85rem; margin-top: 6px;">Elegí el alimento o snack preferido de tu mascota y sumalo.</p>
      </div>
    `;
    if (totalEl) totalEl.textContent = "$0";
    return;
  }

  let total = 0;

  body.innerHTML = cart.map((item, idx) => {
    const itemSubtotal = item.price * item.quantity;
    total += itemSubtotal;

    return `
      <div class="cart-item">
        <img class="cart-item-img" referrerpolicy="no-referrer" src="${item.image}" alt="${item.name}"
             onerror="this.src='https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80'">
        <div class="cart-item-info">
          <div class="cart-item-title">${item.name}</div>
          <div class="cart-item-pres">${item.presentation}</div>
          <div class="cart-item-price">$${item.price.toLocaleString('es-AR')} c/u</div>
        </div>
        <div class="cart-item-controls">
          <button class="btn-qty" onclick="changeCartQty(${idx}, -1)">-</button>
          <span class="qty-num">${item.quantity}</span>
          <button class="btn-qty" onclick="changeCartQty(${idx}, 1)">+</button>
          <button class="btn-remove-item" title="Eliminar" onclick="removeCartItem(${idx})">✕</button>
        </div>
      </div>
    `;
  }).join('');

  if (totalEl) totalEl.textContent = `$${total.toLocaleString('es-AR')}`;
}

async function checkoutWhatsApp() {
  if (cart.length === 0) return;

  const total = cart.reduce((acc, i) => acc + (i.price * i.quantity), 0);

  const orderPayload = {
    customer_name: "Cliente Web WhatsApp",
    customer_phone: CONFIG.waNumber,
    customer_address: "A coordinar por WhatsApp",
    payment_method: "A convenir",
    subtotal: total,
    total: total,
    notes: "Pedido iniciado desde catálogo web",
    items: cart.map(i => ({
      product_name: i.name,
      presentation_name: i.presentation,
      unit_price: i.price,
      quantity: i.quantity,
      subtotal: i.price * i.quantity
    }))
  };

  const orderResult = await API.submitOrder(orderPayload);
  const orderCode = orderResult.order_code || "PEDIDO-WEB";

  let msg = `🐶 *¡HOLA ${CONFIG.storeName.toUpperCase()}! QUIERO REALIZAR UN PEDIDO* 🐱\n`;
  msg += `📋 *Código de Pedido:* ${orderCode}\n`;
  msg += `─────────────────────────\n`;
  
  cart.forEach((i) => {
    msg += `• *${i.quantity}x* ${i.name} (${i.presentation})\n`;
    msg += `   Subtotal: $${(i.price * i.quantity).toLocaleString('es-AR')}\n`;
  });

  msg += `─────────────────────────\n`;
  msg += `✅ *TOTAL ESTIMADO:* $${total.toLocaleString('es-AR')}\n\n`;
  msg += `📍 *Dirección de Entrega:* \n`;
  msg += `¿Podemos coordinar la entrega y el horario? ¡Muchas gracias!`;

  const waUrl = `https://wa.me/${CONFIG.waNumber}?text=${encodeURIComponent(msg)}`;
  window.open(waUrl, '_blank');
}

function askProductWhatsApp(productId) {
  const p = PRODUCTS_DB.find(item => item.id === productId);
  if (!p) return;
  const presIdx = selectedPresIndices[productId] || 0;
  const pres = (p.presentations && p.presentations[presIdx]) ? p.presentations[presIdx] : "";
  const price = (p.prices && p.prices[presIdx]) ? p.prices[presIdx] : 0;

  let msg = `Hola ${CONFIG.storeName}, quería consultar disponibilidad de:\n`;
  msg += `🐾 *${p.name}* (${pres})\n`;
  msg += `Precio: $${price.toLocaleString('es-AR')}\n\n`;
  msg += `¿Podemos coordinar para el envío?`;

  const waUrl = `https://wa.me/${CONFIG.waNumber}?text=${encodeURIComponent(msg)}`;
  window.open(waUrl, '_blank');
}

function filterCategory(cat, subcat = 'todas') {
  catalogFilters.category = cat;
  catalogFilters.subcat = subcat;
  catalogFilters.promoOnly = (cat === 'promociones');

  // Actualizar chip activo en la barra de categorías del catálogo
  document.querySelectorAll('.cat-chip').forEach(chip => {
    const txt = chip.textContent.toLowerCase();
    let isMatch = false;
    if (cat === 'todos' && txt.includes('todo')) isMatch = true;
    else if (cat === 'granja' && txt.includes('granja')) isMatch = true;
    else if (cat === 'peces' && txt.includes('peces')) isMatch = true;
    else if (cat === 'plagas' && txt.includes('plagas')) isMatch = true;
    else if (cat === 'perros' && txt.includes('perros')) isMatch = true;
    else if (cat === 'gatos' && txt.includes('gatos')) isMatch = true;
    else if (cat === 'snacks' && txt.includes('snacks')) isMatch = true;
    else if (cat === 'higiene' && txt.includes('piedras')) isMatch = true;
    else if (cat === 'farmacia' && txt.includes('farmacia')) isMatch = true;
    else if (cat === 'promociones' && txt.includes('especiales')) isMatch = true;
    chip.classList.toggle('active', isMatch);
  });
  
  const catalogSection = document.getElementById('catalogSection');
  if (catalogSection) {
    catalogSection.scrollIntoView({ behavior: 'smooth' });
  }

  loadCatalogAndRender();
}

function filterBySearch(text) {
  catalogFilters.search = text;
  const catalogSection = document.getElementById('catalogSection');
  if (catalogSection && text.length > 1) {
    catalogSection.scrollIntoView({ behavior: 'smooth' });
  }
  loadCatalogAndRender();
}

function resetFilters() {
  catalogFilters = {
    category: 'todos',
    subcat: 'todas',
    breed_size: 'todas',
    promoOnly: false,
    search: ''
  };
  const searchInput = document.getElementById('searchInput');
  if (searchInput) searchInput.value = '';
  document.querySelectorAll('.cat-chip').forEach((c, idx) => {
    c.classList.toggle('active', idx === 0);
  });
  loadCatalogAndRender();
}

// -------------------------------------------------------------
// PANEL DE ADMINISTRACIÓN PROTEGIDO POR PIN Y GESTOR DE IMÁGENES
// -------------------------------------------------------------
let isAdminAuthenticated = false;

function openSettingsModal() {
  if (!isAdminAuthenticated) {
    openAdminPinModal();
    return;
  }
  showAdminSettingsContent();
}

function openAdminPinModal() {
  const modal = document.getElementById('adminPinModal');
  const inputPin = document.getElementById('inputSecurityPin');
  const errorMsg = document.getElementById('pinErrorMsg');
  const storeNameEl = document.getElementById('pinModalStoreName');
  if (storeNameEl) storeNameEl.textContent = CONFIG.storeName;
  if (errorMsg) errorMsg.textContent = '';
  if (inputPin) inputPin.value = '';
  if (modal) {
    modal.style.display = 'flex';
    modal.classList.add('open');
  }
  document.body.style.overflow = 'hidden';
  setTimeout(() => {
    if (inputPin) inputPin.focus();
  }, 100);
}

function closeAdminPinModal() {
  const modal = document.getElementById('adminPinModal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('open');
  }
  document.body.style.overflow = '';
  if (window.location.hash === '#admin') {
    history.replaceState(null, null, ' ');
  }
}

function closeAdminPinModalOnBackdrop(event) {
  if (event.target.id === 'adminPinModal') {
    closeAdminPinModal();
  }
}

function verifyAdminPin() {
  const inputPin = document.getElementById('inputSecurityPin');
  const errorMsg = document.getElementById('pinErrorMsg');
  const pin = inputPin ? inputPin.value.trim() : '';

  if (pin === CONFIG.adminPin) {
    isAdminAuthenticated = true;
    closeAdminPinModal();
    showAdminSettingsContent();
  } else {
    if (errorMsg) errorMsg.textContent = '❌ PIN incorrecto. Acceso restringido al titular.';
    if (inputPin) {
      inputPin.value = '';
      inputPin.focus();
    }
  }
}

function showAdminSettingsContent() {
  document.getElementById('inputStoreName').value = CONFIG.storeName;
  document.getElementById('inputWaNumber').value = CONFIG.waNumber;
  document.getElementById('inputInstagram').value = CONFIG.instagram;
  document.getElementById('selectMarginPolicy').value = CONFIG.marginPolicy;
  document.getElementById('inputAdminPin').value = CONFIG.adminPin;
  
  // Actualizar métricas del monitor de visitas
  const localAnalytics = JSON.parse(localStorage.getItem('maly_analytics') || '{}');
  const uVisitorsEl = document.getElementById('statUniqueVisitors');
  const tViewsEl = document.getElementById('statTotalViews');
  const todayViewsEl = document.getElementById('statTodayViews');
  const lastVisitEl = document.getElementById('statLastVisit');

  if (uVisitorsEl) uVisitorsEl.textContent = (localAnalytics.sessions ? localAnalytics.sessions.length : 1);
  if (tViewsEl) tViewsEl.textContent = (localAnalytics.total_views || 1);
  if (todayViewsEl) todayViewsEl.textContent = (localAnalytics.today_views || 1);
  if (lastVisitEl) lastVisitEl.textContent = (localAnalytics.last_visit || 'Reciente');

  API.getStats().then(stats => {
    if (!stats) return;

    if (stats.total_views !== undefined && tViewsEl) {
      tViewsEl.textContent = stats.total_views;
    }
    if (stats.unique_visitors !== undefined && uVisitorsEl) {
      uVisitorsEl.textContent = stats.unique_visitors;
    }
    if (stats.today_views !== undefined && todayViewsEl) {
      todayViewsEl.textContent = stats.today_views;
    }
    if (stats.last_visit !== undefined && lastVisitEl) {
      lastVisitEl.textContent = stats.last_visit;
    }

    const statsBox = document.getElementById('dbStatsDisplay');
    if (statsBox) {
      statsBox.innerHTML = `
        <div style="background: white; border: 1px solid #e2e8f0; padding: 12px; border-radius: 8px; font-size: 0.85rem; line-height: 1.6;">
          <strong>📦 Catálogo MalyPetShop en Base de Datos:</strong><br>
          • Artículos cargados: <strong>${stats.total_products}</strong><br>
          • Presentaciones y tamaños: <strong>${stats.total_variants}</strong><br>
          • Marcas registradas: <strong>${stats.total_brands}</strong><br>
          • Categorías principales: <strong>${stats.total_categories}</strong>
        </div>
      `;
    }
  });

  renderAdminProductImageList();
  switchAdminTab('general');

  const modal = document.getElementById('settingsModal');
  if (modal) {
    modal.style.display = 'flex';
    modal.classList.add('open');
  }
  document.body.style.overflow = 'hidden';
}

function closeSettingsModal() {
  const modal = document.getElementById('settingsModal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('open');
  }
  document.body.style.overflow = '';
  if (window.location.hash === '#admin') {
    history.replaceState(null, null, ' ');
  }
}

function switchAdminTab(tabName) {
  const tabGeneral = document.getElementById('adminTabGeneral');
  const tabImages = document.getElementById('adminTabImages');
  const tabCreate = document.getElementById('adminTabCreateProduct');
  const btnTabGeneral = document.getElementById('btnTabGeneral');
  const btnTabImages = document.getElementById('btnTabImages');
  const btnTabCreate = document.getElementById('btnTabCreateProduct');

  if (tabGeneral) tabGeneral.style.display = (tabName === 'general') ? 'block' : 'none';
  if (tabImages) tabImages.style.display = (tabName === 'images') ? 'block' : 'none';
  if (tabCreate) tabCreate.style.display = (tabName === 'createProduct') ? 'block' : 'none';

  if (btnTabGeneral) btnTabGeneral.classList.toggle('active', tabName === 'general');
  if (btnTabImages) btnTabImages.classList.toggle('active', tabName === 'images');
  if (btnTabCreate) btnTabCreate.classList.toggle('active', tabName === 'createProduct');

  if (tabName === 'images') {
    renderAdminProductImageList();
  } else if (tabName === 'createProduct') {
    initProductCreatorForm();
  }
}

// -------------------------------------------------------------
// CARGA MANUAL DE PRODUCTOS EN ADMINISTRACIÓN (CRUD)
// -------------------------------------------------------------
let createProductCustomImage = '';

function getEffectiveMarginPercent(weightKg = 15) {
  if (CONFIG.marginPolicy === 'recommended') {
    if (weightKg >= 18) return 20.0;
    if (weightKg >= 10) return 22.0;
    return 25.0;
  }
  return parseFloat(CONFIG.marginPolicy) || 25.0;
}

function initProductCreatorForm() {
  // Cargar lista de marcas únicas en el datalist
  const datalist = document.getElementById('brandDatalist');
  if (datalist) {
    const brands = Array.from(new Set(PRODUCTS_DB.map(p => p.brand_name || p.brand).filter(Boolean))).sort();
    datalist.innerHTML = brands.map(b => `<option value="${b}">`).join('');
  }

  // Actualizar etiqueta del margen comercial
  const marginLabel = document.getElementById('createProdMarginLabel');
  if (marginLabel) {
    marginLabel.textContent = CONFIG.marginPolicy === 'recommended' ? 'Recomendado (20-25%)' : `${CONFIG.marginPolicy}%`;
  }

  // Inicializar filas de presentaciones si está vacío
  const rowsContainer = document.getElementById('createProdPresRows');
  if (rowsContainer && rowsContainer.children.length === 0) {
    addPresentationRow('Bolsa 15 kg', 15, '');
  }
}

function addPresentationRow(name = '', weight = 15, cost = '') {
  const tbody = document.getElementById('createProdPresRows');
  if (!tbody) return;

  const rowId = `pres_row_${Date.now()}_${Math.floor(Math.random()*1000)}`;
  const tr = document.createElement('tr');
  tr.id = rowId;

  tr.innerHTML = `
    <td>
      <input type="text" class="pres-name-input" value="${name}" placeholder="Ej: Bolsa 15 kg / 250 cc" required>
    </td>
    <td>
      <input type="number" step="0.01" class="pres-weight-input" value="${weight}" placeholder="15" oninput="recalculatePresentationRow(this)">
    </td>
    <td>
      <input type="number" step="10" class="pres-cost-input" value="${cost}" placeholder="Ej: 35000" required oninput="recalculatePresentationRow(this)">
    </td>
    <td>
      <span class="badge-calc-sale">$0</span>
      <span class="badge-calc-profit">Ganancia: $0</span>
    </td>
    <td style="text-align: center;">
      <button type="button" onclick="removePresentationRow('${rowId}')" style="background: none; border: none; color: #dc2626; cursor: pointer; font-size: 1.1rem;" title="Eliminar presentación">🗑️</button>
    </td>
  `;

  tbody.appendChild(tr);
  if (cost) {
    const costInput = tr.querySelector('.pres-cost-input');
    recalculatePresentationRow(costInput);
  }
}

function removePresentationRow(rowId) {
  const row = document.getElementById(rowId);
  const tbody = document.getElementById('createProdPresRows');
  if (tbody && tbody.children.length <= 1) {
    alert("El producto debe tener al menos una presentación.");
    return;
  }
  if (row) row.remove();
}

function recalculatePresentationRow(inputEl) {
  const tr = inputEl.closest('tr');
  if (!tr) return;

  const weightInput = tr.querySelector('.pres-weight-input');
  const costInput = tr.querySelector('.pres-cost-input');
  const saleBadge = tr.querySelector('.badge-calc-sale');
  const profitBadge = tr.querySelector('.badge-calc-profit');

  const weight = parseFloat(weightInput.value) || 1.0;
  const cost = parseFloat(costInput.value) || 0;
  const marginPct = getEffectiveMarginPercent(weight);

  const salePrice = Math.round(cost * (1.0 + marginPct / 100.0));
  const profit = salePrice - cost;

  if (saleBadge) saleBadge.textContent = `$${salePrice.toLocaleString('es-AR')}`;
  if (profitBadge) profitBadge.textContent = `Ganancia: +$${profit.toLocaleString('es-AR')} (${marginPct}%)`;
}

function previewCreateProductImage() {
  const url = document.getElementById('createProdImgUrl').value.trim();
  const box = document.getElementById('createProdImgPreviewBox');
  const img = document.getElementById('createProdImgPreview');
  if (url) {
    createProductCustomImage = url;
    img.src = url;
    box.style.display = 'flex';
  } else {
    createProductCustomImage = '';
    box.style.display = 'none';
  }
}

function handleCreateProductFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    createProductCustomImage = e.target.result;
    const box = document.getElementById('createProdImgPreviewBox');
    const img = document.getElementById('createProdImgPreview');
    img.src = createProductCustomImage;
    box.style.display = 'flex';
    document.getElementById('createProdImgUrl').value = '';
  };
  reader.readAsDataURL(file);
}

function clearCreateProductImage() {
  createProductCustomImage = '';
  document.getElementById('createProdImgUrl').value = '';
  document.getElementById('createProdImgFile').value = '';
  const box = document.getElementById('createProdImgPreviewBox');
  if (box) box.style.display = 'none';
}

async function handleCreateProductSubmit() {
  const statusMsg = document.getElementById('createProdStatusMsg');
  const name = document.getElementById('createProdName').value.trim();
  const brand = document.getElementById('createProdBrand').value.trim();
  const category = document.getElementById('createProdCategory').value;
  const pet_type = document.getElementById('createProdPetType').value;
  const subcat = document.getElementById('createProdSubcat').value.trim() || 'general';
  const breed_size = document.getElementById('createProdBreedSize').value;
  const badge = document.getElementById('createProdBadge').value.trim();
  const is_featured = document.getElementById('createProdIsFeatured').checked;
  const is_promo = document.getElementById('createProdIsPromo').checked;
  const description = document.getElementById('createProdDesc').value.trim();

  if (!name) {
    alert("Por favor, ingresá el nombre del producto.");
    return;
  }

  // Recopilar presentaciones
  const trs = document.querySelectorAll('#createProdPresRows tr');
  const variants = [];
  trs.forEach((tr, idx) => {
    const pName = tr.querySelector('.pres-name-input').value.trim();
    const weight = parseFloat(tr.querySelector('.pres-weight-input').value) || 1.0;
    const cost = parseFloat(tr.querySelector('.pres-cost-input').value) || 0;
    if (pName && cost > 0) {
      const marginPct = getEffectiveMarginPercent(weight);
      const sale = Math.round(cost * (1.0 + marginPct / 100.0));
      const list = is_promo ? Math.round(sale * 1.15) : sale;
      variants.push({
        presentation_name: pName,
        weight_kg: weight,
        cost_price: cost,
        margin_percent: marginPct,
        sale_price: sale,
        list_price: list,
        is_default: idx === 0 ? 1 : 0
      });
    }
  });

  if (variants.length === 0) {
    alert("Tenés que agregar al menos una presentación con costo proveedor válido.");
    return;
  }

  // Imagen por defecto según categoría si no se subió una
  let finalImage = createProductCustomImage || document.getElementById('createProdImgUrl').value.trim();
  if (!finalImage) {
    if (category === 'peces') finalImage = 'https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?w=600&auto=format&fit=crop&q=80';
    else if (category === 'granja') finalImage = 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=600&auto=format&fit=crop&q=80';
    else if (category === 'plagas') finalImage = 'https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80';
    else if (category === 'gatos') finalImage = 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80';
    else finalImage = 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80';
  }

  const payload = {
    name,
    brand: brand || 'General',
    brand_name: brand || 'General',
    category,
    category_slug: category,
    pet_type,
    subcat,
    breed_size,
    badge,
    is_featured,
    is_promo,
    promo_tag: is_promo ? 'PRECIO ESPECIAL' : '',
    description,
    image_url: finalImage,
    variants
  };

  statusMsg.style.color = '#0284c7';
  statusMsg.textContent = 'Guardando producto en el catálogo...';

  try {
    const res = await API.createProduct(payload);
    statusMsg.style.color = '#15803d';
    statusMsg.textContent = `✓ ¡Producto "${name}" agregado con éxito!`;

    // Recargar catálogo y actualizar vistas inmediatamente
    await loadCatalogAndRender();

    // Limpiar formulario después de 1.5 segundos
    setTimeout(() => {
      document.getElementById('formCreateProduct').reset();
      clearCreateProductImage();
      document.getElementById('createProdPresRows').innerHTML = '';
      addPresentationRow('Bolsa 15 kg', 15, '');
      statusMsg.textContent = '';
      alert(`✓ ¡Producto "${name}" cargado exitosamente!
Ya está visible en la tienda para la venta.`);
    }, 1200);

  } catch (err) {
    statusMsg.style.color = '#dc2626';
    statusMsg.textContent = `Error al guardar: ${err.message}`;
  }
}


// RENDERIZADO DEL GESTOR DE IMÁGENES DENTRO DEL PANEL ADMIN
let currentAdminCategoryFilter = 'todos';

function filterAdminProductCategory(cat, btnEl) {
  currentAdminCategoryFilter = cat;
  document.querySelectorAll('.admin-filter-chips .cat-chip').forEach(c => c.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  const searchInput = document.getElementById('adminImageSearchInput');
  const q = searchInput ? searchInput.value : '';
  renderAdminProductImageList(q);
}

function renderAdminProductImageList(filterQuery = '') {
  const listContainer = document.getElementById('adminProductImageRows');
  if (!listContainer) return;

  let prods = [...PRODUCTS_DB];

  // Filtro por categoría en admin
  if (currentAdminCategoryFilter !== 'todos') {
    if (currentAdminCategoryFilter === 'ofertas') {
      prods = prods.filter(p => p.is_promo || p.promo);
    } else {
      prods = prods.filter(p => p.category_slug === currentAdminCategoryFilter || p.category === currentAdminCategoryFilter);
    }
  }

  // Filtro por búsqueda
  if (filterQuery) {
    const q = filterQuery.toLowerCase().trim();
    prods = prods.filter(p => 
      p.name.toLowerCase().includes(q) || 
      (p.brand_name || p.brand || '').toLowerCase().includes(q) ||
      (p.category_name || p.category || '').toLowerCase().includes(q)
    );
  }

  if (prods.length === 0) {
    listContainer.innerHTML = `<div style="text-align:center; padding: 30px; color: #64748b;">No se encontraron productos con esos filtros.</div>`;
    return;
  }

  listContainer.innerHTML = prods.map(p => {
    const presList = p.presentations || ["Única"];
    const costsList = p.costs || [];
    const pricesList = p.prices || [];

    const presChips = presList.map((pr, idx) => {
      const c = costsList[idx] ? `$${costsList[idx].toLocaleString('es-AR')}` : '-';
      const v = pricesList[idx] ? `$${pricesList[idx].toLocaleString('es-AR')}` : '-';
      return `<span class="admin-pres-chip">${pr}: Costo ${c} ➔ <strong>Venta ${v}</strong></span>`;
    }).join('');

    return `
      <div class="admin-prod-card" id="admin-row-${p.id}">
        <div class="admin-prod-main">
          <div class="admin-prod-img-box">
            <img src="${p.image_url}" referrerpolicy="no-referrer" class="admin-prod-thumb" id="admin-thumb-${p.id}" alt="${p.name}"
                 onerror="this.src='https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80'">
            <label class="admin-btn-quick-photo" title="Cambiar foto desde archivo">
              📷 Foto
              <input type="file" accept="image/*" style="display:none" onchange="handleAdminFileUpload(${p.id}, this)">
            </label>
          </div>

          <div class="admin-prod-info">
            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
              <span class="admin-badge brand">${p.brand_name || p.brand}</span>
              <span class="admin-badge cat">${p.category_name || p.category}</span>
              ${(p.is_promo || p.promo) ? '<span class="admin-badge promo">🔥 OFERTA</span>' : ''}
              ${(p.is_featured || p.featured) ? '<span class="admin-badge featured">⭐ DESTACADO</span>' : ''}
              ${p.badge ? `<span class="admin-badge tag">${p.badge}</span>` : ''}
            </div>

            <div class="admin-prod-name" style="font-size: 0.95rem; font-weight: 700; color: #1e293b;">${p.name}</div>

            <div class="admin-prod-pres-list">
              ${presChips}
            </div>

            <div class="admin-quick-img-bar">
              <input type="text" id="admin-input-url-${p.id}" placeholder="Pegar URL de foto..." 
                     value="${p.image_url && !p.image_url.startsWith('data:') ? p.image_url : ''}" class="admin-input-url">
              
              <button type="button" class="btn-save-img" onclick="saveAdminProductImage(${p.id})">
                💾 Guardar Foto
              </button>

              <button type="button" class="btn-edit-prod-full" onclick="openEditProductModal(${p.id})">
                ✏️ Editar Características & Precios
              </button>
            </div>
            <div id="admin-save-status-${p.id}" class="admin-save-status"></div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// -------------------------------------------------------------
// MODAL DE EDICIÓN COMPLETA DE PRODUCTO EN ADMINISTRACIÓN
// -------------------------------------------------------------
let editProductCustomImage = '';

function openEditProductModal(productId) {
  const p = PRODUCTS_DB.find(item => item.id === productId);
  if (!p) return;

  document.getElementById('editProdId').value = p.id;
  document.getElementById('editProdName').value = p.name || '';
  document.getElementById('editProdBrand').value = p.brand_name || p.brand || '';
  document.getElementById('editProdCategory').value = p.category_slug || p.category || 'perros';
  document.getElementById('editProdPetType').value = p.pet_type || 'perros';
  document.getElementById('editProdSubcat').value = p.subcat || 'adulto';
  document.getElementById('editProdBreedSize').value = p.breed_size || 'todas';
  document.getElementById('editProdBadge').value = p.badge || '';
  document.getElementById('editProdIsFeatured').checked = Boolean(p.is_featured || p.featured);
  document.getElementById('editProdIsPromo').checked = Boolean(p.is_promo || p.promo);
  document.getElementById('editProdDesc').value = p.description || p.desc || '';

  editProductCustomImage = '';
  const imgUrlInput = document.getElementById('editProdImgUrl');
  const imgPreview = document.getElementById('editProdImgPreview');
  const imgUrlVal = p.image_url && !p.image_url.startsWith('data:') ? p.image_url : '';
  imgUrlInput.value = imgUrlVal;
  imgPreview.src = p.image_url || '';

  // Actualizar etiqueta del margen
  const marginLabel = document.getElementById('editProdMarginLabel');
  if (marginLabel) {
    marginLabel.textContent = CONFIG.marginPolicy === 'recommended' ? 'Recomendado (20-25%)' : `${CONFIG.marginPolicy}%`;
  }

  // Cargar presentaciones
  const tbody = document.getElementById('editProdPresRows');
  tbody.innerHTML = '';
  const presList = p.presentations || ["Única"];
  const costsList = p.costs || [1000];
  const variants = p.variants || [];

  presList.forEach((presName, idx) => {
    const cost = costsList[idx] || (variants[idx] && variants[idx].cost_price) || 1000;
    const weight = (variants[idx] && variants[idx].weight_kg) || 15;
    addEditPresentationRow(presName, weight, cost);
  });

  document.getElementById('editProdStatusMsg').textContent = '';
  document.getElementById('editProductModal').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function closeEditProductModal() {
  const modal = document.getElementById('editProductModal');
  if (modal) modal.style.display = 'none';
  const settingsModal = document.getElementById('settingsModal');
  if (!settingsModal || !settingsModal.classList.contains('open')) {
    document.body.style.overflow = '';
  }
}

function closeEditProductModalOnBackdrop(event) {
  if (event.target.id === 'editProductModal') {
    closeEditProductModal();
  }
}

function previewEditProductImage() {
  const url = document.getElementById('editProdImgUrl').value.trim();
  const img = document.getElementById('editProdImgPreview');
  if (url) {
    editProductCustomImage = url;
    img.src = url;
  }
}

function handleEditProductFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    editProductCustomImage = e.target.result;
    document.getElementById('editProdImgPreview').src = editProductCustomImage;
    document.getElementById('editProdImgUrl').value = '';
  };
  reader.readAsDataURL(file);
}

function addEditPresentationRow(name = '', weight = 15, cost = '') {
  const tbody = document.getElementById('editProdPresRows');
  if (!tbody) return;

  const rowId = `edit_pres_row_${Date.now()}_${Math.floor(Math.random()*1000)}`;
  const tr = document.createElement('tr');
  tr.id = rowId;

  tr.innerHTML = `
    <td>
      <input type="text" class="pres-name-input" value="${name}" placeholder="Ej: Bolsa 15 kg / 250 cc" required>
    </td>
    <td>
      <input type="number" step="0.01" class="pres-weight-input" value="${weight}" placeholder="15" oninput="recalculateEditPresentationRow(this)">
    </td>
    <td>
      <input type="number" step="10" class="pres-cost-input" value="${cost}" placeholder="Ej: 35000" required oninput="recalculateEditPresentationRow(this)">
    </td>
    <td>
      <span class="badge-calc-sale">$0</span>
      <span class="badge-calc-profit">Ganancia: $0</span>
    </td>
    <td style="text-align: center;">
      <button type="button" onclick="removeEditPresentationRow('${rowId}')" style="background: none; border: none; color: #dc2626; cursor: pointer; font-size: 1.1rem;" title="Eliminar presentación">🗑️</button>
    </td>
  `;

  tbody.appendChild(tr);
  if (cost) {
    const costInput = tr.querySelector('.pres-cost-input');
    recalculateEditPresentationRow(costInput);
  }
}

function removeEditPresentationRow(rowId) {
  const tbody = document.getElementById('editProdPresRows');
  if (tbody && tbody.children.length <= 1) {
    alert("El producto debe tener al menos una presentación.");
    return;
  }
  const row = document.getElementById(rowId);
  if (row) row.remove();
}

function recalculateEditPresentationRow(inputEl) {
  const tr = inputEl.closest('tr');
  if (!tr) return;

  const weightInput = tr.querySelector('.pres-weight-input');
  const costInput = tr.querySelector('.pres-cost-input');
  const saleBadge = tr.querySelector('.badge-calc-sale');
  const profitBadge = tr.querySelector('.badge-calc-profit');

  const weight = parseFloat(weightInput.value) || 1.0;
  const cost = parseFloat(costInput.value) || 0;
  const marginPct = getEffectiveMarginPercent(weight);

  const salePrice = Math.round(cost * (1.0 + marginPct / 100.0));
  const profit = salePrice - cost;

  if (saleBadge) saleBadge.textContent = `$${salePrice.toLocaleString('es-AR')}`;
  if (profitBadge) profitBadge.textContent = `Ganancia: +$${profit.toLocaleString('es-AR')} (${marginPct}%)`;
}

async function handleEditProductSubmit() {
  const productId = parseInt(document.getElementById('editProdId').value);
  const statusMsg = document.getElementById('editProdStatusMsg');
  const name = document.getElementById('editProdName').value.trim();
  const brand = document.getElementById('editProdBrand').value.trim();
  const category = document.getElementById('editProdCategory').value;
  const pet_type = document.getElementById('editProdPetType').value;
  const subcat = document.getElementById('editProdSubcat').value.trim() || 'general';
  const breed_size = document.getElementById('editProdBreedSize').value;
  const badge = document.getElementById('editProdBadge').value.trim();
  const is_featured = document.getElementById('editProdIsFeatured').checked;
  const is_promo = document.getElementById('editProdIsPromo').checked;
  const description = document.getElementById('editProdDesc').value.trim();

  if (!name) {
    alert("Por favor, ingresá el nombre del producto.");
    return;
  }

  // Recopilar presentaciones editadas
  const trs = document.querySelectorAll('#editProdPresRows tr');
  const variants = [];
  trs.forEach((tr, idx) => {
    const pName = tr.querySelector('.pres-name-input').value.trim();
    const weight = parseFloat(tr.querySelector('.pres-weight-input').value) || 1.0;
    const cost = parseFloat(tr.querySelector('.pres-cost-input').value) || 0;
    if (pName && cost > 0) {
      const marginPct = getEffectiveMarginPercent(weight);
      const sale = Math.round(cost * (1.0 + marginPct / 100.0));
      const list = is_promo ? Math.round(sale * 1.15) : sale;
      variants.push({
        presentation_name: pName,
        weight_kg: weight,
        cost_price: cost,
        margin_percent: marginPct,
        sale_price: sale,
        list_price: list,
        is_default: idx === 0 ? 1 : 0
      });
    }
  });

  if (variants.length === 0) {
    alert("El producto debe tener al menos una presentación con costo válido.");
    return;
  }

  let finalImage = editProductCustomImage || document.getElementById('editProdImgUrl').value.trim();
  if (!finalImage) {
    const pOrig = PRODUCTS_DB.find(item => item.id === productId);
    finalImage = pOrig ? pOrig.image_url : '';
  }

  const payload = {
    name,
    brand,
    brand_name: brand,
    category,
    category_slug: category,
    pet_type,
    subcat,
    breed_size,
    badge,
    is_featured,
    is_promo,
    promo_tag: is_promo ? 'PRECIO ESPECIAL' : '',
    description,
    image_url: finalImage,
    variants
  };

  statusMsg.style.color = '#0284c7';
  statusMsg.textContent = 'Guardando cambios del producto...';

  try {
    await API.updateProduct(productId, payload);
    statusMsg.style.color = '#15803d';
    statusMsg.textContent = `✓ ¡Producto "${name}" actualizado con éxito!`;

    // Recargar catálogo y actualizar vistas inmediatamente
    await loadCatalogAndRender();
    renderAdminProductImageList();

    setTimeout(() => {
      closeEditProductModal();
      alert(`✓ ¡Producto "${name}" modificado con éxito!\nLos precios y características ya están actualizados en toda la tienda.`);
    }, 800);
  } catch (err) {
    statusMsg.style.color = '#dc2626';
    statusMsg.textContent = `Error al actualizar: ${err.message}`;
  }
}

function handleAdminFileUpload(productId, fileInput) {
  const file = fileInput.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    const dataUrl = e.target.result;
    const thumb = document.getElementById(`admin-thumb-${productId}`);
    const inputUrl = document.getElementById(`admin-input-url-${productId}`);
    
    if (thumb) thumb.src = dataUrl;
    if (inputUrl) {
      inputUrl.value = "";
      inputUrl.dataset.dataUrl = dataUrl;
    }

    const statusEl = document.getElementById(`admin-save-status-${productId}`);
    if (statusEl) {
      statusEl.textContent = `Archivo "${file.name}" cargado. Hacé clic en "Guardar Foto".`;
      statusEl.style.color = '#0284c7';
    }
  };
  reader.readAsDataURL(file);
}

async function saveAdminProductImage(productId) {
  const inputUrl = document.getElementById(`admin-input-url-${productId}`);
  const thumb = document.getElementById(`admin-thumb-${productId}`);
  const statusEl = document.getElementById(`admin-save-status-${productId}`);

  let newImage = '';
  if (inputUrl.dataset.dataUrl) {
    newImage = inputUrl.dataset.dataUrl;
  } else if (inputUrl.value.trim()) {
    newImage = inputUrl.value.trim();
  }

  if (!newImage) {
    alert("Por favor ingresá una URL o seleccioná un archivo de imagen.");
    return;
  }

  statusEl.textContent = "Guardando...";
  statusEl.style.color = '#64748b';

  await API.updateProductImage(productId, newImage);

  // Actualizar en el objeto en memoria
  const p = PRODUCTS_DB.find(prod => prod.id === productId);
  if (p) p.image_url = newImage;

  // Actualizar todas las imágenes del producto en la tienda
  document.querySelectorAll(`.product-card[data-product-id="${productId}"] img.card-img`).forEach(img => {
    img.src = newImage;
  });

  if (thumb) thumb.src = newImage;

  statusEl.textContent = "✅ ¡Foto guardada y actualizada con éxito!";
  statusEl.style.color = '#16a34a';

  setTimeout(() => {
    if (statusEl) statusEl.textContent = "";
  }, 4000);
}

async function saveSettings() {
  const newName = document.getElementById('inputStoreName').value.trim() || "Maly Petshop";
  const newWa = document.getElementById('inputWaNumber').value.trim() || "5491158549783";
  const newIg = document.getElementById('inputInstagram').value.trim() || "maly.petshop";
  const newMargin = document.getElementById('selectMarginPolicy').value;
  const newPin = document.getElementById('inputAdminPin').value.trim() || "1234";

  CONFIG.storeName = newName;
  CONFIG.waNumber = newWa;
  CONFIG.instagram = newIg;
  CONFIG.marginPolicy = newMargin;
  CONFIG.adminPin = newPin;

  localStorage.setItem('petshop_name', CONFIG.storeName);
  localStorage.setItem('petshop_wa', CONFIG.waNumber);
  localStorage.setItem('petshop_ig', CONFIG.instagram);
  localStorage.setItem('petshop_margin_policy', CONFIG.marginPolicy);
  localStorage.setItem('petshop_admin_pin', CONFIG.adminPin);

  // Guardar en backend SQLite si está disponible
  await API.updateSetting('store_name', CONFIG.storeName);
  await API.updateSetting('whatsapp_number', CONFIG.waNumber);
  await API.updateSetting('instagram_user', CONFIG.instagram);
  await API.updateSetting('margin_policy', CONFIG.marginPolicy);
  await API.updateSetting('admin_pin', CONFIG.adminPin);

  applyConfigToDOM();
  closeSettingsModal();
  loadCatalogAndRender();
  alert(`✅ Configuración guardada correctamente.\nNombre de la tienda: "${CONFIG.storeName}"`);
}

function applyConfigToDOM() {
  const name = (CONFIG.storeName || "Maly Petshop").trim();
  document.title = `${name} | Alimentos Balanceados & Accesorios`;

  const headerLogo = document.getElementById('brandLogoText');
  if (headerLogo) {
    headerLogo.textContent = name;
  } else {
    const headerTitle = document.getElementById('brandHeaderTitle');
    if (headerTitle) {
      headerTitle.innerHTML = `<span class="logo-icon">🐾</span> <span id="brandLogoText">${name}</span>`;
    }
  }

  const footerLogo = document.getElementById('footerBrandLogoText');
  if (footerLogo) {
    footerLogo.textContent = name;
  } else {
    const footerTitle = document.getElementById('footerBrandTitle');
    if (footerTitle) {
      footerTitle.innerHTML = `<span class="logo-icon">🐾</span> <span id="footerBrandLogoText">${name}</span>`;
    }
  }

  const footerCopyright = document.getElementById('footerCopyrightStoreName');
  if (footerCopyright) {
    footerCopyright.textContent = name;
  }

  const pinStoreName = document.getElementById('pinModalStoreName');
  if (pinStoreName) {
    pinStoreName.textContent = name;
  }

  const inputName = document.getElementById('inputStoreName');
  if (inputName) {
    inputName.value = name;
  }

  const inputIgEl = document.getElementById('inputInstagram');
  if (inputIgEl && document.activeElement !== inputIgEl) {
    inputIgEl.value = (CONFIG.instagram || 'maly.petshop').trim();
  }

  // Actualizar enlace de Instagram dinámicamente con el usuario ingresado en admin
  const igVal = (CONFIG.instagram || 'maly.petshop').trim();
  const igUrl = getInstagramUrl(igVal);
  const cleanHandle = igVal.replace(/^https?:\/\/(www\.)?instagram\.com\//, '').replace(/^@+/, '').replace(/\/$/, '');

  const headerIg = document.getElementById('headerIgBtn');
  if (headerIg) {
    headerIg.href = igUrl;
    headerIg.title = cleanHandle ? `Seguinos en Instagram: @${cleanHandle}` : 'Seguinos en Instagram';
  }

  const footerIg = document.getElementById('footerIgLink');
  if (footerIg) {
    footerIg.href = igUrl;
  }

  const footerIgUser = document.getElementById('footerIgUser');
  if (footerIgUser) {
    footerIgUser.textContent = cleanHandle ? `@${cleanHandle}` : '@instagram';
  }

  // Actualizar enlace de WhatsApp de la cabecera
  const headerWa = document.getElementById('headerWaBtn');
  if (headerWa) {
    headerWa.href = `https://wa.me/${CONFIG.waNumber}`;
  }
}

function setupEventListeners() {
  // Sincronización en tiempo real del usuario de Instagram al tipear
  const inputIg = document.getElementById('inputInstagram');
  if (inputIg) {
    inputIg.addEventListener('input', (e) => {
      const val = e.target.value.trim();
      CONFIG.instagram = val || 'maly.petshop';
      localStorage.setItem('petshop_ig', CONFIG.instagram);
      applyConfigToDOM();
    });
  }

  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        filterBySearch(e.target.value);
      }, 300);
    });
  }

  // Buscador dentro del gestor de imágenes de admin
  const adminSearch = document.getElementById('adminImageSearchInput');
  if (adminSearch) {
    adminSearch.addEventListener('input', (e) => {
      renderAdminProductImageList(e.target.value);
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeCartDrawer();
      closeSettingsModal();
    }
  });
}


async function exportCatalogForVercel() {
  const statusEl = document.getElementById('exportVercelStatusMsg');
  if (statusEl) {
    statusEl.innerHTML = '⏳ Sincronizando catálogo...';
    statusEl.style.color = '#0284c7';
  }

  try {
    const res = await fetch('/api/admin/sync-catalog', { method: 'POST' });
    if (res.ok) {
      if (statusEl) {
        statusEl.innerHTML = '✅ <strong>¡Catálogo sincronizado exitosamente!</strong> Se actualizó <code>public/js/catalog-data.js</code> con todas tus fotos y productos. Ya podés subir la carpeta <code>public</code> a Vercel.';
        statusEl.style.color = '#15803d';
      }
      return;
    }
  } catch (e) {
    console.log('No backend connection, fallback to browser export');
  }

  try {
    const dataStr = "const LOCAL_CATALOG = " + JSON.stringify(LOCAL_CATALOG, null, 2) + ";\n";
    const blob = new Blob([dataStr], { type: "application/javascript" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "catalog-data.js";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    if (statusEl) {
      statusEl.innerHTML = '📥 <strong>Se descargó el archivo catalog-data.js</strong> con todas tus fotos. Pegalo adentro de la carpeta <code>public/js/</code> antes de subir a Vercel.';
      statusEl.style.color = '#0284c7';
    }
  } catch (err) {
    if (statusEl) {
      statusEl.innerHTML = '❌ Error al exportar: ' + err.message;
      statusEl.style.color = '#dc2626';
    }
  }
}

