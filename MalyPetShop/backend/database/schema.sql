-- ====================================================================
-- SCHEMA DE BASE DE DATOS: PELLEGRINI PETSHOP
-- Motor: SQLite 3 / Relacional
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. Categorías Principales
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    pet_type TEXT NOT NULL CHECK (pet_type IN ('perro', 'gato', 'general')),
    icon TEXT,
    display_order INTEGER DEFAULT 0
);

-- 2. Marcas
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    tier TEXT DEFAULT 'Premium',
    origin TEXT DEFAULT 'Nacional'
);

-- 3. Productos (Catálogo)
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    brand_id INTEGER NOT NULL REFERENCES brands(id) ON DELETE RESTRICT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    pet_type TEXT NOT NULL CHECK (pet_type IN ('perros', 'gatos', 'ambos')),
    subcat TEXT NOT NULL,
    breed_size TEXT DEFAULT 'todas',
    badge TEXT,
    image_url TEXT,
    is_featured BOOLEAN DEFAULT 0,
    is_promo BOOLEAN DEFAULT 0,
    promo_tag TEXT,
    active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Variantes / Presentaciones de Producto
CREATE TABLE IF NOT EXISTS product_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    presentation_name TEXT NOT NULL,
    weight_kg REAL NOT NULL,
    cost_price REAL NOT NULL,
    margin_percent REAL NOT NULL,
    sale_price REAL NOT NULL,
    cash_price REAL NOT NULL,
    stock_qty INTEGER DEFAULT 50,
    sku TEXT,
    is_default BOOLEAN DEFAULT 0
);

-- 5. Órdenes / Consultas de Compra
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_code TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    customer_address TEXT,
    payment_method TEXT DEFAULT 'efectivo',
    subtotal REAL NOT NULL,
    discount REAL DEFAULT 0,
    total REAL NOT NULL,
    status TEXT DEFAULT 'pendiente',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Ítems de la Orden
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    variant_id INTEGER REFERENCES product_variants(id),
    product_name TEXT NOT NULL,
    presentation_name TEXT NOT NULL,
    unit_price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    subtotal REAL NOT NULL
);

-- 7. Configuración General de la Tienda
CREATE TABLE IF NOT EXISTS store_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT
);

-- Índices de Rendimiento
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand_id);
CREATE INDEX IF NOT EXISTS idx_products_pet_type ON products(pet_type);
CREATE INDEX IF NOT EXISTS idx_products_active ON products(active);
CREATE INDEX IF NOT EXISTS idx_variants_product ON product_variants(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at);
