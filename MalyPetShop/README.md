# 🐾 MalyPetShop - Tienda Online de Alimentos Balanceados & Accesorios

Sistema de comercio electrónico y catálogo interactivo de nutrición animal para **MalyPetShop** (Ciudad Evita y alrededores).

## 🚀 Inicio Rápido (En 1 Clic)

### En Windows:
Hacé doble clic en `run.bat` o ejecutá:
```cmd
python run.py
```

### En Mac / Linux:
```bash
python3 run.py
```

Abrí tu navegador en: **http://localhost:8000**

---

## 🌟 Características Principales

1. **Catálogo Completo de 144 Productos:**
   - Alimentos secos, húmedos, cachorros, adultos, razas pequeñas, medianas y grandes.
   - Marcas líderes: Royal Canin, Purina Pro Plan, Eukanuba, Sieger, Dog Chow, Cat Chow, Pedigree, Whiskas, Excellent, etc.
   - Granja, aves, peces, conejos, piedras sanitarias y farmacia/belleza.

2. **Cálculo de Precios y Márgenes en Tiempo Real:**
   - Selector dinámico de presentaciones (kilos, gramos, unidades).
   - Cálculo automático de precios de venta a partir del costo proveedor y margen comercial.

3. **Panel de Administración (Acceso con PIN '1234'):**
   - Atajo de teclado: `Ctrl + Shift + A` o ingresando a `http://localhost:8000/#admin`.
   - **Monitor de Visitas y Tráfico Web:** Estadísticas en vivo de visitantes únicos, páginas vistas, visitas del día y último acceso.
   - **Gestión & Edición de Productos:** Modificá fotos, precios, presentaciones y características de cualquier producto en vivo.
   - **Ajustes:** Personalizá nombre de la tienda, número de WhatsApp para pedidos, usuario de Instagram y margen comercial.

4. **Pedidos Directos por WhatsApp:**
   - Carrito/Bolsa de compra que genera el mensaje listo para enviar con el detalle de los productos, cantidades y total.

---

## 🌐 Cómo Publicar la Tienda en Internet

### Opción 1: Publicación Gratuita con Vercel o Netlify (Recomendado)
El catálogo y la tienda funcionan de forma 100% autónoma en el frontend:
1. Creá una cuenta gratuita en [Vercel](https://vercel.com) o [Netlify](https://netlify.com).
2. Subí los archivos de la carpeta `public` (o conectá tu repositorio de GitHub).
3. ¡Listo! Te asignará una dirección web pública gratuita como `https://malypetshop.vercel.app`.

### Opción 2: Publicación con Backend Python en Render.com o Railway
1. Creá un servicio web en [Render.com](https://render.com) o [Railway.app].
2. Comando de inicio: `python backend/server_builtin.py`.
3. Te entregará una URL como `https://malypetshop.onrender.com`.

### Opción 3: Dominio Propio (.com.ar o .com)
- Para tener **www.malypetshop.com.ar**, registralo en [Nic.ar](https://nic.ar).
- Podés vincularlo fácilmente a Vercel o Render configurando los DNS indicados.
