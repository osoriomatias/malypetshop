# -*- coding: utf-8 -*-
"""
MalyPetShop - Lanzador Universal Inteligente
Detecta automáticamente las dependencias del entorno:
- Si FastAPI y Uvicorn están instalados -> Ejecuta el backend FastAPI con Swagger Docs interactivo.
- Si no están instalados -> Ejecuta el Servidor Nativo (Python Standard Library + SQLite) con CERO dependencias.
"""
import os
import sys
import webbrowser

def main():
    print("=" * 65)
    print(" 🐾 MALYPETSHOP - INICIANDO SISTEMA CON BASE DE DATOS")
    print("=" * 65)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(current_dir, "backend")
    db_file = os.path.join(backend_dir, "database", "petshop.db")
    seed_script = os.path.join(backend_dir, "database", "seed.py")

    # 1. Asegurar base de datos SQLite
    if not os.path.exists(db_file):
        print("📦 Base de datos no encontrada. Inicializando SQLite y cargando catálogo...")
        os.system(f'"{sys.executable}" "{seed_script}"')
    else:
        print("✅ Base de datos SQLite conectada (backend/database/petshop.db).")

    # 2. Comprobar si uvicorn y fastapi están instalados
    has_uvicorn = False
    try:
        import uvicorn
        import fastapi
        has_uvicorn = True
    except ImportError:
        has_uvicorn = False

    port = 8000
    print("\n🌐 Acceso al sistema:")
    print(f"   👉 Tienda Web:           http://localhost:{port}")
    if has_uvicorn:
        print(f"   👉 Swagger API Docs:     http://localhost:{port}/docs")
    else:
        print("   👉 Servidor:             Nativo Python Standard Library (0 dependencias externas)")
        print("   💡 Nota: Si deseás activar la documentación interactiva Swagger, ejecutá:")
        print("            pip install -r requirements.txt")
    print(f"   👉 API Health Check:     http://localhost:{port}/api/health")
    print("\nPresione Ctrl+C para detener el servidor.\n")

    # Abrir navegador automáticamente evitando caché previa
    try:
        import time
        webbrowser.open(f"http://localhost:{port}/?v={int(time.time())}")
    except Exception:
        pass

    # 3. Iniciar servidor correspondiente
    if has_uvicorn:
        import uvicorn
        sys.path.append(backend_dir)
        uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, app_dir=backend_dir)
    else:
        sys.path.append(backend_dir)
        from server_builtin import PetShopHandler, sync_catalog_js
        sync_catalog_js()
        from http.server import HTTPServer
        server = HTTPServer(("0.0.0.0", port), PetShopHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

if __name__ == "__main__":
    main()
