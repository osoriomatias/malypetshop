# -*- coding: utf-8 -*-
"""
Pellegrini PetShop - Backend REST API (FastAPI)
Arquitectura limpia para la gestión del catálogo, variantes de peso, precios y órdenes.
"""
import os
import sys
import uuid
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Configuración de importación de base de datos
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)
from database import db

app = FastAPI(
    title="Pellegrini PetShop - API REST",
    description="API empresarial para la gestión del catálogo de alimentos balanceados, variantes de peso y pedidos.",
    version="2.0.0"
)

# Habilitar CORS para permitir consumo desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# MODELOS PYDANTIC
# -------------------------------------------------------------
class VariantInput(BaseModel):
    presentation_name: str
    weight_kg: float = 1.0
    cost_price: float
    margin_percent: float = 25.0
    sale_price: Optional[float] = None
    list_price: Optional[float] = None
    stock_qty: int = 50
    sku: Optional[str] = None
    is_default: bool = False

class ProductCreate(BaseModel):
    name: str
    category_id: Optional[int] = None
    category: Optional[str] = None
    brand_id: Optional[int] = None
    brand: Optional[str] = None
    description: Optional[str] = ""
    pet_type: str = "ambos"
    subcat: str = "general"
    breed_size: str = "todas"
    badge: Optional[str] = None
    image_url: Optional[str] = ""
    is_featured: bool = False
    is_promo: bool = False
    promo_tag: Optional[str] = None
    variants: List[VariantInput] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    description: Optional[str] = None
    pet_type: Optional[str] = None
    subcat: Optional[str] = None
    breed_size: Optional[str] = None
    badge: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: Optional[bool] = None
    is_promo: Optional[bool] = None
    promo_tag: Optional[str] = None
    active: Optional[bool] = None
    variants: Optional[List[VariantInput]] = None

class OrderItemInput(BaseModel):
    variant_id: Optional[int] = None
    product_name: str
    presentation_name: str
    unit_price: float
    quantity: int
    subtotal: float

class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: Optional[str] = ""
    payment_method: str = "efectivo"
    subtotal: float
    discount: float = 0.0
    total: float
    notes: Optional[str] = ""
    items: List[OrderItemInput]

class SettingUpdate(BaseModel):
    value: str

# -------------------------------------------------------------
# RUTAS DE PRODUCTOS Y CATÁLOGO
# -------------------------------------------------------------
@app.get("/api/health", tags=["Sistema"])
def health_check():
    """Verifica el estado del servicio y conexión a SQLite."""
    prod_count = db.query_one("SELECT COUNT(*) as c FROM products WHERE active = 1")["c"]
    return {
        "status": "healthy",
        "service": "Pellegrini PetShop API",
        "database": "SQLite 3",
        "active_products": prod_count
    }

@app.get("/api/stats", tags=["Dashboard"])
def get_stats():
    """Estadísticas completas del catálogo y negocio."""
    prods = db.query_one("SELECT COUNT(*) as c FROM products WHERE active = 1")["c"]
    variants = db.query_one("SELECT COUNT(*) as c FROM product_variants")["c"]
    brands = db.query_one("SELECT COUNT(*) as c FROM brands")["c"]
    cats = db.query_one("SELECT COUNT(*) as c FROM categories")["c"]
    orders = db.query_one("SELECT COUNT(*) as c FROM orders")["c"]
    return {
        "total_products": prods,
        "total_variants": variants,
        "total_brands": brands,
        "total_categories": cats,
        "total_orders": orders
    }

@app.get("/api/products", tags=["Catálogo"])
def list_products(
    category: Optional[str] = Query(None, description="Slug de categoría (perros, gatos, snacks, farmacia, promociones)"),
    pet_type: Optional[str] = Query(None, description="perros, gatos, ambos"),
    subcat: Optional[str] = Query(None, description="adulto, cachorro, senior, higiene, snacks"),
    breed_size: Optional[str] = Query(None, description="pequeña, mediana, grande, todas"),
    brand: Optional[str] = Query(None, description="Nombre de marca"),
    is_featured: Optional[bool] = Query(None, description="Solo destacados"),
    is_promo: Optional[bool] = Query(None, description="Solo promociones"),
    search: Optional[str] = Query(None, description="Búsqueda por texto libre"),
    margin_policy: Optional[str] = Query("recommended", description="recommended, 10, 15, 20, 25, 30")
):
    """
    Retorna el listado completo de productos con sus variantes de peso y precios calculados.
    Permite filtrar por categoría, tipo de mascota, tamaño de raza, promociones y texto.
    """
    sql = """
        SELECT 
            p.id, p.name, p.slug, p.description, p.pet_type, p.subcat, p.breed_size,
            p.badge, p.image_url, p.is_featured, p.is_promo, p.promo_tag, p.active,
            c.id as category_id, c.name as category_name, c.slug as category_slug, c.icon as category_icon,
            b.id as brand_id, b.name as brand_name, b.tier as brand_tier
        FROM products p
        JOIN categories c ON p.category_id = c.id
        JOIN brands b ON p.brand_id = b.id
        WHERE p.active = 1
    """
    params = []

    if category and category != "todos":
        if category == "promociones":
            sql += " AND p.is_promo = 1"
        else:
            sql += " AND c.slug = ?"
            params.append(category)

    if pet_type and pet_type != "todos":
        sql += " AND (p.pet_type = ? OR p.pet_type = 'ambos')"
        params.append(pet_type)

    if subcat and subcat != "todas":
        sql += " AND p.subcat = ?"
        params.append(subcat)

    if breed_size and breed_size != "todas":
        sql += " AND (p.breed_size = ? OR p.breed_size = 'todas')"
        params.append(breed_size)

    if brand and brand != "todas":
        sql += " AND b.name = ?"
        params.append(brand)

    if is_featured:
        sql += " AND p.is_featured = 1"

    if is_promo:
        sql += " AND p.is_promo = 1"

    if search:
        search_term = f"%{search.strip().lower()}%"
        sql += " AND (LOWER(p.name) LIKE ? OR LOWER(b.name) LIKE ? OR LOWER(p.description) LIKE ?)"
        params.extend([search_term, search_term, search_term])

    sql += " ORDER BY p.is_featured DESC, p.id ASC"
    products = db.query_all(sql, params)

    # Obtenemos todas las variantes de los productos encontrados
    if not products:
        return []

    prod_ids = [p["id"] for p in products]
    placeholders = ",".join(["?"] * len(prod_ids))
    variants_sql = f"""
        SELECT id, product_id, presentation_name, weight_kg, cost_price, margin_percent,
               sale_price, cash_price, stock_qty, sku, is_default
        FROM product_variants
        WHERE product_id IN ({placeholders})
        ORDER BY weight_kg ASC, id ASC
    """
    variants_rows = db.query_all(variants_sql, prod_ids)

    # Agrupamos variantes por producto
    variants_by_prod = {}
    for v in variants_rows:
        pid = v["product_id"]
        if pid not in variants_by_prod:
            variants_by_prod[pid] = []

        # Si el usuario solicitó una política de margen plana específica, recalculamos precios
        cost = v["cost_price"]
        orig_margin = v["margin_percent"]
        if margin_policy and margin_policy != "recommended":
            try:
                forced_m = float(margin_policy)
                eff_sale = round(cost * (1.0 + forced_m / 100.0))
                eff_cash = round(eff_sale * 0.90)
                v["effective_margin"] = forced_m
                v["effective_sale_price"] = eff_sale
                v["effective_cash_price"] = eff_cash
            except ValueError:
                v["effective_margin"] = orig_margin
                v["effective_sale_price"] = v["sale_price"]
                v["effective_cash_price"] = v["cash_price"]
        else:
            v["effective_margin"] = orig_margin
            v["effective_sale_price"] = v["sale_price"]
            v["effective_cash_price"] = v["cash_price"]

        variants_by_prod[pid].append(v)

    # Ensamblamos productos con sus variantes y lista simple de presentaciones para la UI
    for p in products:
        vars_list = variants_by_prod.get(p["id"], [])
        p["variants"] = vars_list
        p["presentations"] = [v["presentation_name"] for v in vars_list]
        p["costs"] = [v["cost_price"] for v in vars_list]
        p["prices"] = [v["effective_sale_price"] for v in vars_list]
        p["cash_prices"] = [v["effective_cash_price"] for v in vars_list]

    return products

@app.get("/api/products/{product_id}", tags=["Catálogo"])
def get_product(product_id: int):
    """Retorna el detalle de un producto específico con todas sus variantes."""
    sql = """
        SELECT 
            p.id, p.name, p.slug, p.description, p.pet_type, p.subcat, p.breed_size,
            p.badge, p.image_url, p.is_featured, p.is_promo, p.promo_tag, p.active,
            c.id as category_id, c.name as category_name, c.slug as category_slug, c.icon as category_icon,
            b.id as brand_id, b.name as brand_name, b.tier as brand_tier
        FROM products p
        JOIN categories c ON p.category_id = c.id
        JOIN brands b ON p.brand_id = b.id
        WHERE p.id = ?
    """
    product = db.query_one(sql, (product_id,))
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    variants = db.query_all("""
        SELECT id, presentation_name, weight_kg, cost_price, margin_percent,
               sale_price, cash_price, stock_qty, sku, is_default
        FROM product_variants
        WHERE product_id = ?
        ORDER BY weight_kg ASC
    """, (product_id,))

    product["variants"] = variants
    product["presentations"] = [v["presentation_name"] for v in variants]
    product["costs"] = [v["cost_price"] for v in variants]
    product["prices"] = [v["sale_price"] for v in variants]
    product["cash_prices"] = [v["cash_price"] for v in variants]
    return product

@app.post("/api/products", status_code=status.HTTP_201_CREATED, tags=["Gestión de Catálogo (CRUD)"])
def create_product(prod: ProductCreate):
    """Crea un nuevo producto en la base de datos con sus variantes de peso."""
    import re
    # Categoría
    cat_id = prod.category_id
    if not cat_id:
        c_slug = prod.category or "perros"
        row = db.query_one("SELECT id FROM categories WHERE slug = ?", (c_slug,))
        if row:
            cat_id = row["id"]
        else:
            cat_id = db.execute_write("INSERT INTO categories (slug, name, pet_type, icon, display_order) VALUES (?, ?, ?, '📦', 10)",
                                      (c_slug, c_slug.capitalize(), prod.pet_type))

    # Marca
    b_id = prod.brand_id
    if not b_id:
        b_name = (prod.brand or "General").strip()
        row = db.query_one("SELECT id FROM brands WHERE name = ?", (b_name,))
        if row:
            b_id = row["id"]
        else:
            b_id = db.execute_write("INSERT INTO brands (name, tier, origin) VALUES (?, 'Estándar', 'Nacional')", (b_name,))

    base_slug = re.sub(r'[^a-z0-9]+', '-', prod.name.lower()).strip('-')
    slug = base_slug
    idx = 1
    while db.query_one("SELECT id FROM products WHERE slug = ?", (slug,)):
        slug = f"{base_slug}-{idx}"
        idx += 1

    insert_prod_sql = """
        INSERT INTO products (
            category_id, brand_id, name, slug, description, pet_type, subcat,
            breed_size, badge, image_url, is_featured, is_promo, promo_tag, active
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    """
    prod_id = db.execute_write(insert_prod_sql, (
        cat_id, b_id, prod.name, slug, prod.description or "",
        prod.pet_type, prod.subcat, prod.breed_size, prod.badge,
        prod.image_url or "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80",
        1 if prod.is_featured else 0, 1 if prod.is_promo else 0, prod.promo_tag
    ))

    # Variantes
    vars_list = prod.variants
    if not vars_list:
        vars_list = [VariantInput(presentation_name="Unidad", weight_kg=1.0, cost_price=1000.0, margin_percent=25.0, is_default=True)]

    for v in vars_list:
        sale = v.sale_price or round(v.cost_price * (1.0 + (v.margin_percent / 100.0)))
        list_pr = v.list_price or round(sale * 1.15)
        db.execute_write("""
            INSERT INTO product_variants (
                product_id, presentation_name, weight_kg, cost_price, margin_percent,
                sale_price, list_price, stock_qty, sku, is_default
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prod_id, v.presentation_name, v.weight_kg, v.cost_price, v.margin_percent,
            sale, list_pr, v.stock_qty, v.sku or f"SKU-{prod_id}-{v.weight_kg}",
            1 if v.is_default else 0
        ))

    return get_product(prod_id)

@app.put("/api/products/{product_id}", tags=["Gestión de Catálogo (CRUD)"])
def update_product(product_id: int, prod: ProductUpdate):
    """Actualiza datos, estado o variantes de un producto."""
    existing = db.query_one("SELECT id FROM products WHERE id = ?", (product_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    fields = []
    params = []
    data = prod.dict(exclude_unset=True)

    for key in ['name', 'category_id', 'brand_id', 'description', 'pet_type', 'subcat', 'breed_size', 'badge', 'image_url', 'is_featured', 'is_promo', 'promo_tag', 'active']:
        if key in data:
            fields.append(f"{key} = ?")
            val = data[key]
            if isinstance(val, bool):
                val = 1 if val else 0
            params.append(val)

    if fields:
        params.append(product_id)
        db.execute_write(f"UPDATE products SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", params)

    if prod.variants is not None:
        db.execute_write("DELETE FROM product_variants WHERE product_id = ?", (product_id,))
        for v in prod.variants:
            sale = round(v.cost_price * (1.0 + (v.margin_percent / 100.0)))
            cash = round(sale * 0.90)
            db.execute_write("""
                INSERT INTO product_variants (
                    product_id, presentation_name, weight_kg, cost_price, margin_percent,
                    sale_price, cash_price, stock_qty, sku, is_default
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_id, v.presentation_name, v.weight_kg, v.cost_price, v.margin_percent,
                sale, cash, v.stock_qty, v.sku, 1 if v.is_default else 0
            ))

    return get_product(product_id)

@app.delete("/api/products/{product_id}", tags=["Gestión de Catálogo (CRUD)"])
def delete_product(product_id: int):
    """Desactiva lógicamente un producto del catálogo."""
    existing = db.query_one("SELECT id FROM products WHERE id = ?", (product_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.execute_write("UPDATE products SET active = 0 WHERE id = ?", (product_id,))
    return {"message": "Producto desactivado exitosamente", "product_id": product_id}

# -------------------------------------------------------------
# CATEGORÍAS Y MARCAS
# -------------------------------------------------------------
@app.get("/api/categories", tags=["Metadatos"])
def get_categories():
    """Retorna categorías con conteo de productos activos."""
    sql = """
        SELECT c.id, c.slug, c.name, c.pet_type, c.icon, c.display_order,
               COUNT(p.id) as products_count
        FROM categories c
        LEFT JOIN products p ON p.category_id = c.id AND p.active = 1
        GROUP BY c.id
        ORDER BY c.display_order ASC
    """
    return db.query_all(sql)

@app.get("/api/brands", tags=["Metadatos"])
def get_brands():
    """Retorna marcas con conteo de productos."""
    sql = """
        SELECT b.id, b.name, b.tier, b.origin,
               COUNT(p.id) as products_count
        FROM brands b
        LEFT JOIN products p ON p.brand_id = b.id AND p.active = 1
        GROUP BY b.id
        ORDER BY b.name ASC
    """
    return db.query_all(sql)

# -------------------------------------------------------------
# CONFIGURACIÓN DE LA TIENDA
# -------------------------------------------------------------
@app.get("/api/settings", tags=["Configuración"])
def get_settings():
    """Retorna todas las claves de configuración de la tienda."""
    rows = db.query_all("SELECT key, value, description FROM store_settings")
    return {r["key"]: r["value"] for r in rows}

@app.put("/api/settings/{key}", tags=["Configuración"])
def update_setting(key: str, payload: SettingUpdate):
    """Actualiza una clave de configuración (ej: store_name, whatsapp_number, margin_policy)."""
    db.execute_write("INSERT INTO store_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, payload.value))
    return {"key": key, "value": payload.value, "updated": True}

# -------------------------------------------------------------
# ÓRDENES Y VENTAS
# -------------------------------------------------------------
@app.post("/api/orders", status_code=status.HTTP_201_CREATED, tags=["Órdenes"])
def create_order(order: OrderCreate):
    """Registra una orden de compra o consulta enviada por el cliente."""
    order_code = f"ORD-{uuid.uuid4().hex[:6].upper()}"
    order_id = db.execute_write("""
        INSERT INTO orders (
            order_code, customer_name, customer_phone, customer_address,
            payment_method, subtotal, discount, total, status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pendiente', ?)
    """, (
        order_code, order.customer_name, order.customer_phone, order.customer_address,
        order.payment_method, order.subtotal, order.discount, order.total, order.notes
    ))

    for item in order.items:
        db.execute_write("""
            INSERT INTO order_items (
                order_id, variant_id, product_name, presentation_name,
                unit_price, quantity, subtotal
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, item.variant_id, item.product_name, item.presentation_name,
            item.unit_price, item.quantity, item.subtotal
        ))

    return {
        "order_id": order_id,
        "order_code": order_code,
        "customer_name": order.customer_name,
        "total": order.total,
        "status": "pendiente",
        "message": "Orden registrada exitosamente en la base de datos."
    }

@app.get("/api/orders", tags=["Órdenes"])
def list_orders():
    """Retorna las órdenes registradas con sus ítems para el panel de administración."""
    orders = db.query_all("SELECT * FROM orders ORDER BY created_at DESC LIMIT 50")
    for o in orders:
        items = db.query_all("SELECT * FROM order_items WHERE order_id = ?", (o["id"],))
        o["items"] = items
    return orders

# -------------------------------------------------------------
# MONTAJE DE ARCHIVOS ESTÁTICOS FRONTEND
# -------------------------------------------------------------
PUBLIC_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "public")
if os.path.exists(PUBLIC_DIR):
    app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="public")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
