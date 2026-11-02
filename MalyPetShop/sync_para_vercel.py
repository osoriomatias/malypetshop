import sqlite3, json, os

db_path = '/working_dir/c_1bb7fb2872f81c14/MalyPetShop/backend/database/petshop.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
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

out_path = '/working_dir/c_1bb7fb2872f81c14/MalyPetShop/public/js/catalog-data.js'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('const LOCAL_CATALOG = ' + json.dumps(products, indent=2, ensure_ascii=False) + ';\nif (typeof window !== "undefined") window.LOCAL_CATALOG = LOCAL_CATALOG;\n')

print(f'Successfully synchronized {len(products)} products to {out_path}!')
