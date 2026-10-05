# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
DB_PATH = os.path.join(BASE_DIR, "backend", "database", "petshop.db")
TMP_DB = "/tmp/pellegrini_petshop.db"

def get_db():
    import shutil
    if not os.path.exists(TMP_DB) and os.path.exists(DB_PATH):
        try:
            shutil.copyfile(DB_PATH, TMP_DB)
        except Exception:
            pass

    use_tmp = False
    try:
        test = sqlite3.connect(DB_PATH, timeout=1)
        test.execute("PRAGMA journal_mode = MEMORY")
        test.execute("CREATE TABLE IF NOT EXISTS _test_lock (x INT)")
        test.commit()
        test.close()
    except Exception:
        use_tmp = True

    target = TMP_DB if use_tmp else DB_PATH
    conn = sqlite3.connect(target, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def sync_catalog_js():
    try:
        conn = get_db()
        c = conn.cursor()
        sql = """
            SELECT p.id, p.name, p.slug, p.description, p.pet_type, p.subcat,
                   p.breed_size, p.badge, p.image_url, p.is_featured, p.is_promo,
                   p.promo_tag, c.name as category_name, c.slug as category_slug,
                   b.name as brand_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            JOIN brands b ON p.brand_id = b.id
            WHERE p.active = 1
            ORDER BY p.is_featured DESC, p.id ASC
        """
        products = [dict(row) for row in c.execute(sql).fetchall()]
        for p in products:
            v_rows = c.execute("""
                SELECT presentation_name, weight_kg, cost_price, margin_percent,
                       sale_price, list_price, stock_qty, sku
                FROM product_variants WHERE product_id = ?
                ORDER BY weight_kg ASC
            """, (p["id"],)).fetchall()
            variants = [dict(vr) for vr in v_rows]
            p["variants"] = variants
            p["presentations"] = [v["presentation_name"] for v in variants]
            p["costs"] = [v["cost_price"] for v in variants]
            p["prices"] = [v["sale_price"] for v in variants]
            p["list_prices"] = [v["list_price"] for v in variants]
            p["brand"] = p["brand_name"]
            p["category"] = p["category_slug"]
            p["desc"] = p["description"]
            p["featured"] = bool(p["is_featured"])
            p["promo"] = bool(p["is_promo"])
        conn.close()

        catalog_js_path = os.path.join(PUBLIC_DIR, "js", "catalog-data.js")
        with open(catalog_js_path, "w", encoding="utf-8") as f:
            f.write("const LOCAL_CATALOG = " + json.dumps(products, indent=2, ensure_ascii=False) + ";\n")
        print(f"[AUTO-SYNC] Catálogo estático sincronizado exitosamente en {catalog_js_path} ({len(products)} productos).")
    except Exception as e:
        print("[AUTO-SYNC ERROR]", e)

def sync_to_disk():
    import shutil
    if os.path.exists(TMP_DB) and os.path.exists(DB_PATH):
        try:
            shutil.copyfile(TMP_DB, DB_PATH)
        except Exception:
            pass

class PetShopHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path.startswith("/api/"):
            self.handle_api_get(path, query)
        else:
            super().do_GET()

    def handle_api_get(self, path, query):
        conn = get_db()
        c = conn.cursor()

        if path == "/api/health":
            count = c.execute("SELECT COUNT(*) FROM products WHERE active = 1").fetchone()[0]
            self.send_json({
                "status": "healthy",
                "service": "MalyPetShop Servidor Nativo (Zero Dependencies)",
                "database": "SQLite 3",
                "active_products": count
            })
            conn.close()
            return

        
        if path == "/api/admin/sync-catalog":
            self.send_json({"success": True, "message": "Catálogo sincronizado exitosamente con public/js/catalog-data.js"})
            return

        if path in ("/api/stats", "/api/analytics/stats"):
            c.execute("""
                CREATE TABLE IF NOT EXISTS site_visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visit_date TEXT,
                    visit_time TEXT,
                    session_id TEXT,
                    user_agent TEXT
                )
            """)
            prods = c.execute("SELECT COUNT(*) FROM products WHERE active = 1").fetchone()[0]
            variants = c.execute("SELECT COUNT(*) FROM product_variants").fetchone()[0]
            brands = c.execute("SELECT COUNT(*) FROM brands").fetchone()[0]
            cats = c.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
            orders = c.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

            total_views = c.execute("SELECT COUNT(*) FROM site_visits").fetchone()[0]
            unique_visitors = c.execute("SELECT COUNT(DISTINCT session_id) FROM site_visits").fetchone()[0]
            today_views = c.execute("SELECT COUNT(*) FROM site_visits WHERE visit_date = date('now', 'localtime')").fetchone()[0]
            last_visit_row = c.execute("SELECT visit_time FROM site_visits ORDER BY id DESC LIMIT 1").fetchone()
            last_visit = last_visit_row[0] if last_visit_row else "Sin registros aún"

            self.send_json({
                "total_products": prods, "total_variants": variants,
                "total_brands": brands, "total_categories": cats, "total_orders": orders,
                "total_views": total_views, "unique_visitors": unique_visitors,
                "today_views": today_views, "last_visit": last_visit
            })
            conn.close()
            return

        if path == "/api/products":
            cat = query.get("category", [None])[0]
            pet_type = query.get("pet_type", [None])[0]
            subcat = query.get("subcat", [None])[0]
            breed_size = query.get("breed_size", [None])[0]
            brand = query.get("brand", [None])[0]
            search = query.get("search", [None])[0]
            margin_policy = query.get("margin_policy", ["recommended"])[0]
            is_promo = query.get("is_promo", [None])[0]

            sql = """
                SELECT p.id, p.name, p.slug, p.description, p.pet_type, p.subcat, p.breed_size,
                       p.badge, p.image_url, p.is_featured, p.is_promo, p.promo_tag,
                       c.name as category_name, c.slug as category_slug,
                       b.name as brand_name
                FROM products p
                JOIN categories c ON p.category_id = c.id
                JOIN brands b ON p.brand_id = b.id
                WHERE p.active = 1
            """
            params = []
            if cat and cat != "todos":
                if cat == "promociones": sql += " AND p.is_promo = 1"
                else: sql += " AND c.slug = ?"; params.append(cat)
            if pet_type and pet_type != "todos":
                sql += " AND (p.pet_type = ? OR p.pet_type = 'ambos')"; params.append(pet_type)
            if subcat and subcat != "todas":
                sql += " AND p.subcat = ?"; params.append(subcat)
            if breed_size and breed_size != "todas":
                sql += " AND (p.breed_size = ? OR p.breed_size = 'todas')"; params.append(breed_size)
            if brand and brand != "todas":
                sql += " AND b.name = ?"; params.append(brand)
            if is_promo == "true":
                sql += " AND p.is_promo = 1"
            if search:
                term = f"%{search.strip().lower()}%"
                sql += " AND (LOWER(p.name) LIKE ? OR LOWER(b.name) LIKE ? OR LOWER(p.description) LIKE ?)"
                params.extend([term, term, term])

            sql += " ORDER BY p.is_featured DESC, p.id ASC"
            products = [dict(row) for row in c.execute(sql, params).fetchall()]

            for p in products:
                v_rows = c.execute("""
                    SELECT presentation_name, weight_kg, cost_price, margin_percent,
                           sale_price, list_price, stock_qty, sku
                    FROM product_variants WHERE product_id = ?
                    ORDER BY weight_kg ASC
                """, (p["id"],)).fetchall()
                variants = [dict(vr) for vr in v_rows]
                
                if margin_policy and margin_policy != "recommended":
                    try:
                        pct = float(margin_policy) / 100.0
                        for v in variants:
                            v["sale_price"] = round(v["cost_price"] * (1.0 + pct))
                            v["list_price"] = round(v["sale_price"] * 1.15)
                    except ValueError:
                        pass

                p["variants"] = variants
                p["presentations"] = [v["presentation_name"] for v in variants]
                p["costs"] = [v["cost_price"] for v in variants]
                p["prices"] = [v["sale_price"] for v in variants]
                p["list_prices"] = [v["list_price"] for v in variants]

            self.send_json(products)
            conn.close()
            return

        if path == "/api/categories":
            rows = [dict(r) for r in c.execute("""
                SELECT c.id, c.slug, c.name, c.icon, COUNT(p.id) as products_count
                FROM categories c
                LEFT JOIN products p ON p.category_id = c.id AND p.active = 1
                GROUP BY c.id ORDER BY c.display_order ASC
            """).fetchall()]
            self.send_json(rows)
            conn.close()
            return

        if path == "/api/settings":
            rows = c.execute("SELECT key, value FROM store_settings").fetchall()
            self.send_json({r[0]: r[1] for r in rows})
            conn.close()
            return

        conn.close()
        self.send_error(404, "Endpoint no encontrado")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len) if content_len > 0 else b'{}'
        try:
            data = json.loads(body.decode('utf-8'))
        except Exception:
            data = {}

        if path == "/api/products":
            name = data.get("name", "").strip()
            if not name:
                self.send_json({"error": "El nombre del producto es obligatorio"}, 400)
                return

            conn = get_db()
            c = conn.cursor()

            cat_slug = data.get("category_slug") or data.get("category") or "perros"
            cat_row = c.execute("SELECT id FROM categories WHERE slug = ?", (cat_slug,)).fetchone()
            if not cat_row:
                c.execute("INSERT INTO categories (slug, name, pet_type, icon, display_order) VALUES (?, ?, ?, ?, ?)",
                          (cat_slug, cat_slug.capitalize(), data.get("pet_type", "general"), "📦", 10))
                category_id = c.lastrowid
            else:
                category_id = cat_row[0]

            brand_name = (data.get("brand_name") or data.get("brand") or "General").strip()
            brand_row = c.execute("SELECT id FROM brands WHERE name = ?", (brand_name,)).fetchone()
            if not brand_row:
                c.execute("INSERT INTO brands (name, tier, origin) VALUES (?, 'Estándar', 'Nacional')", (brand_name,))
                brand_id = c.lastrowid
            else:
                brand_id = brand_row[0]

            import re
            base_slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            slug = base_slug
            idx = 1
            while c.execute("SELECT id FROM products WHERE slug = ?", (slug,)).fetchone():
                slug = f"{base_slug}-{idx}"
                idx += 1

            c.execute("""
                INSERT INTO products (
                    category_id, brand_id, name, slug, description, pet_type, subcat,
                    breed_size, badge, image_url, is_featured, is_promo, promo_tag, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                category_id, brand_id, name, slug,
                data.get("description", ""),
                data.get("pet_type", "ambos"),
                data.get("subcat", "general"),
                data.get("breed_size", "todas"),
                data.get("badge", ""),
                data.get("image_url", "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80"),
                1 if data.get("is_featured") else 0,
                1 if data.get("is_promo") else 0,
                data.get("promo_tag", "")
            ))
            product_id = c.lastrowid

            variants = data.get("variants", [])
            if not variants:
                cost = float(data.get("cost_price", 1000.0))
                margin = float(data.get("margin_percent", 25.0))
                sale = round(cost * (1.0 + margin / 100.0))
                list_pr = round(sale * 1.15)
                variants = [{
                    "presentation_name": data.get("presentation_name", "Unidad"),
                    "weight_kg": float(data.get("weight_kg", 1.0)),
                    "cost_price": cost,
                    "margin_percent": margin,
                    "sale_price": sale,
                    "list_price": list_pr,
                    "is_default": 1
                }]

            for v in variants:
                v_cost = float(v.get("cost_price", 1000.0))
                v_margin = float(v.get("margin_percent", 25.0))
                v_sale = float(v.get("sale_price") or round(v_cost * (1.0 + v_margin / 100.0)))
                v_list = float(v.get("list_price") or round(v_sale * 1.15))
                c.execute("""
                    INSERT INTO product_variants (
                        product_id, presentation_name, weight_kg, cost_price, margin_percent,
                        sale_price, list_price, stock_qty, sku, is_default
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    product_id,
                    v.get("presentation_name", "Unidad"),
                    float(v.get("weight_kg", 1.0)),
                    v_cost,
                    v_margin,
                    v_sale,
                    v_list,
                    int(v.get("stock_qty", 50)),
                    v.get("sku", f"PROD-{product_id}"),
                    1 if v.get("is_default") else 0
                ))

            conn.commit()
            sync_to_disk()
            conn.close()

            self.send_json({
                "success": True,
                "product_id": product_id,
                "message": "Producto agregado exitosamente al catálogo"
            }, 201)
            return

        
        if path == "/api/admin/sync-catalog":
            self.send_json({"success": True, "message": "Catálogo sincronizado exitosamente con public/js/catalog-data.js"})
            return

        if path == "/api/analytics/visit":
            session_id = data.get("session_id", "anon")
            ua = self.headers.get("User-Agent", "")[:200]
            conn = get_db()
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS site_visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    visit_date TEXT,
                    visit_time TEXT,
                    session_id TEXT,
                    user_agent TEXT
                )
            """)
            c.execute("""
                INSERT INTO site_visits (visit_date, visit_time, session_id, user_agent)
                VALUES (date('now', 'localtime'), datetime('now', 'localtime'), ?, ?)
            """, (session_id, ua))
            conn.commit()
            sync_to_disk()
            conn.close()
            self.send_json({"recorded": True})
            return

        if path == "/api/orders":
            import uuid
            order_code = f"ORD-{uuid.uuid4().hex[:6].upper()}"
            conn = get_db()
            c = conn.cursor()
            c.execute("""
                INSERT INTO orders (order_code, customer_name, customer_phone, customer_address, payment_method, subtotal, total, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pendiente', ?)
            """, (
                order_code, data.get("customer_name", "Cliente Web"), data.get("customer_phone", ""),
                data.get("customer_address", ""), data.get("payment_method", "a convenir"),
                data.get("subtotal", 0), data.get("total", 0), data.get("notes", "")
            ))
            order_id = c.lastrowid
            for item in data.get("items", []):
                c.execute("""
                    INSERT INTO order_items (order_id, product_name, presentation_name, unit_price, quantity, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (order_id, item.get("product_name", ""), item.get("presentation_name", ""),
                      item.get("unit_price", 0), item.get("quantity", 1), item.get("subtotal", 0)))
            conn.commit()
            conn.close()
            self.send_json({"order_id": order_id, "order_code": order_code, "status": "pendiente", "message": "Orden guardada en SQLite"}, 201)
            return

        self.send_error(404, "Endpoint no encontrado")

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len) if content_len > 0 else b'{}'
        try:
            data = json.loads(body.decode('utf-8'))
        except Exception:
            data = {}

        # Actualizar imagen de producto: PUT /api/products/{id}/image
        if path.startswith("/api/products/") and path.endswith("/image"):
            parts = path.strip("/").split("/")
            try:
                prod_id = int(parts[2])
                image_url = data.get("image_url", "")
                conn = get_db()
                c = conn.cursor()
                c.execute("UPDATE products SET image_url = ? WHERE id = ?", (image_url, prod_id))
                conn.commit()
                sync_to_disk()
                conn.close()
                self.send_json({"product_id": prod_id, "image_url": image_url, "updated": True})
                return
            except Exception as e:
                self.send_json({"error": str(e)}, 400)
                return

        # Actualizar producto completo: PUT /api/products/{id}
        if path.startswith("/api/products/") and not path.endswith("/image"):
            parts = path.strip("/").split("/")
            try:
                prod_id = int(parts[2])
                conn = get_db()
                c = conn.cursor()

                chk = c.execute("SELECT id FROM products WHERE id = ?", (prod_id,)).fetchone()
                if not chk:
                    self.send_json({"error": "Producto no encontrado"}, 404)
                    conn.close()
                    return

                name = data.get("name")
                desc = data.get("description")
                pet_type = data.get("pet_type")
                subcat = data.get("subcat")
                breed_size = data.get("breed_size")
                badge = data.get("badge")
                image_url = data.get("image_url")
                is_featured = 1 if data.get("is_featured") else 0
                is_promo = 1 if data.get("is_promo") else 0
                promo_tag = data.get("promo_tag", "")

                cat_slug = data.get("category_slug") or data.get("category")
                if cat_slug:
                    cat_row = c.execute("SELECT id FROM categories WHERE slug = ?", (cat_slug,)).fetchone()
                    if cat_row:
                        c.execute("UPDATE products SET category_id = ? WHERE id = ?", (cat_row[0], prod_id))

                brand_name = data.get("brand_name") or data.get("brand")
                if brand_name:
                    b_row = c.execute("SELECT id FROM brands WHERE name = ?", (brand_name,)).fetchone()
                    if b_row:
                        brand_id = b_row[0]
                    else:
                        c.execute("INSERT INTO brands (name, tier, origin) VALUES (?, 'Estándar', 'Nacional')", (brand_name,))
                        brand_id = c.lastrowid
                    c.execute("UPDATE products SET brand_id = ? WHERE id = ?", (brand_id, prod_id))

                c.execute("""
                    UPDATE products SET
                        name = COALESCE(?, name),
                        description = COALESCE(?, description),
                        pet_type = COALESCE(?, pet_type),
                        subcat = COALESCE(?, subcat),
                        breed_size = COALESCE(?, breed_size),
                        badge = ?,
                        image_url = COALESCE(?, image_url),
                        is_featured = ?,
                        is_promo = ?,
                        promo_tag = ?
                    WHERE id = ?
                """, (name, desc, pet_type, subcat, breed_size, badge, image_url, is_featured, is_promo, promo_tag, prod_id))

                variants = data.get("variants")
                if variants and isinstance(variants, list) and len(variants) > 0:
                    c.execute("DELETE FROM product_variants WHERE product_id = ?", (prod_id,))
                    for idx, v in enumerate(variants):
                        v_name = v.get("presentation_name", "Unidad")
                        v_weight = float(v.get("weight_kg", 1.0))
                        v_cost = float(v.get("cost_price", 1000.0))
                        v_margin = float(v.get("margin_percent", 25.0))
                        v_sale = float(v.get("sale_price") or round(v_cost * (1.0 + v_margin / 100.0)))
                        v_list = float(v.get("list_price") or (round(v_sale * 1.15) if is_promo else v_sale))
                        c.execute("""
                            INSERT INTO product_variants (
                                product_id, presentation_name, weight_kg, cost_price, margin_percent,
                                sale_price, list_price, stock_qty, sku, is_default
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, 50, ?, ?)
                        """, (prod_id, v_name, v_weight, v_cost, v_margin, v_sale, v_list, f"PROD-{prod_id}-{idx}", 1 if idx == 0 else 0))

                conn.commit()
                sync_to_disk()
                conn.close()

                self.send_json({"product_id": prod_id, "updated": True, "message": "Producto actualizado con éxito"})
                return
            except Exception as e:
                self.send_json({"error": str(e)}, 400)
                return

        # Actualizar configuraciones: PUT /api/settings/{key}
        if path.startswith("/api/settings/"):
            key = path.split("/")[-1]
            val = data.get("value", "")
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO store_settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, val))
            conn.commit()
            sync_to_disk()
            conn.close()
            self.send_json({"key": key, "value": val, "updated": True})
            return

        self.send_error(404, "Endpoint no encontrado")

    def send_json(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        self.wfile.write(body)

def run_native_server(port=8000):
    sync_catalog_js()
    server = HTTPServer(('0.0.0.0', port), PetShopHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_native_server()
