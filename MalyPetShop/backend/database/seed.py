# -*- coding: utf-8 -*-
"""
Script de inicialización y poblado de la base de datos de Pellegrini PetShop.
Contiene los 144 productos reales del catálogo completo (Lista 28/09/2026),
con todas las fotos personalizadas preservadas.
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'petshop.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

CATEGORIES_DATA = [
  {
    "slug": "perros",
    "name": "Perros",
    "pet_type": "perro",
    "icon": "🐶",
    "display_order": 1
  },
  {
    "slug": "gatos",
    "name": "Gatos",
    "pet_type": "gato",
    "icon": "🐱",
    "display_order": 2
  },
  {
    "slug": "snacks",
    "name": "Snacks & Masticables",
    "pet_type": "general",
    "icon": "🦴",
    "display_order": 3
  },
  {
    "slug": "higiene",
    "name": "Piedras & Sanitarios",
    "pet_type": "gato",
    "icon": "✨",
    "display_order": 4
  },
  {
    "slug": "farmacia",
    "name": "Farmacia & Cuidado",
    "pet_type": "general",
    "icon": "🧴",
    "display_order": 5
  },
  {
    "slug": "promociones",
    "name": "Ofertas & KGs de Regalo",
    "pet_type": "general",
    "icon": "🔥",
    "display_order": 6
  },
  {
    "slug": "peces",
    "name": "Peces & Acuarios",
    "pet_type": "peces",
    "icon": "🐠",
    "display_order": 7
  },
  {
    "slug": "granja",
    "name": "Aves, Semillas & Granja",
    "pet_type": "granja",
    "icon": "🌾",
    "display_order": 8
  },
  {
    "slug": "plagas",
    "name": "Sanidad Ambiental & Plagas",
    "pet_type": "sanidad",
    "icon": "🛡️",
    "display_order": 9
  }
]
BRANDS_DATA = [
  {
    "name": "Royal Canin",
    "tier": "Super Premium",
    "origin": "Francia / Nacional"
  },
  {
    "name": "Pro Plan",
    "tier": "Super Premium",
    "origin": "Nestlé Purina"
  },
  {
    "name": "Eukanuba",
    "tier": "Super Premium",
    "origin": "Mars Petcare"
  },
  {
    "name": "Sieger",
    "tier": "Premium Especial",
    "origin": "Nacional"
  },
  {
    "name": "Dog Chow",
    "tier": "Estándar",
    "origin": "Nestlé Purina"
  },
  {
    "name": "Cat Chow",
    "tier": "Estándar",
    "origin": "Nestlé Purina"
  },
  {
    "name": "Dogui / Gati",
    "tier": "Económica",
    "origin": "Nestlé Purina"
  },
  {
    "name": "Dog Selection",
    "tier": "Premium / Criador",
    "origin": "Nacional"
  },
  {
    "name": "DS Etiqueta Negra",
    "tier": "Super Premium",
    "origin": "Nacional"
  },
  {
    "name": "Pedigree",
    "tier": "Estándar",
    "origin": "Mars Petcare"
  },
  {
    "name": "Whiskas",
    "tier": "Estándar",
    "origin": "Mars Petcare"
  },
  {
    "name": "Temptations",
    "tier": "Snacks Gatos",
    "origin": "Mars Petcare"
  },
  {
    "name": "Dentastix",
    "tier": "Salud Dental",
    "origin": "Mars Petcare"
  },
  {
    "name": "Biscrok",
    "tier": "Galletitas",
    "origin": "Mars Petcare"
  },
  {
    "name": "Excellent",
    "tier": "Super Premium",
    "origin": "Nestlé Purina"
  },
  {
    "name": "Vital Can",
    "tier": "Premium",
    "origin": "Nacional"
  },
  {
    "name": "Protemix",
    "tier": "Premium",
    "origin": "Petfood Saladillo"
  },
  {
    "name": "Gran Campeón",
    "tier": "Económica",
    "origin": "Petfood Saladillo"
  },
  {
    "name": "Tiernitos",
    "tier": "Económica",
    "origin": "Petfood Saladillo"
  },
  {
    "name": "Rosco",
    "tier": "Económica",
    "origin": "Pacha Petfoods"
  },
  {
    "name": "Pacha",
    "tier": "Económica",
    "origin": "Pacha Petfoods"
  },
  {
    "name": "Chacal / Balancín",
    "tier": "Económica",
    "origin": "Nacional"
  },
  {
    "name": "ACA Cooperación",
    "tier": "Económica",
    "origin": "Cooperativa ACA"
  },
  {
    "name": "Raza",
    "tier": "Económica",
    "origin": "Nutripet"
  },
  {
    "name": "Agility",
    "tier": "Premium",
    "origin": "Sieger"
  },
  {
    "name": "Maxxium",
    "tier": "Premium",
    "origin": "Sieger"
  },
  {
    "name": "7 Vidas",
    "tier": "Económica",
    "origin": "Sieger"
  },
  {
    "name": "Huesos & Premios",
    "tier": "Masticables",
    "origin": "Nacional"
  },
  {
    "name": "Absorsol / Piedras",
    "tier": "Higiene Felina",
    "origin": "Nacional"
  },
  {
    "name": "Osspret / Ecthol",
    "tier": "Veterinaria",
    "origin": "Nacional"
  },
  {
    "name": "Shulet",
    "tier": "Peces y Acuarios",
    "origin": "Nacional"
  },
  {
    "name": "Hor-Tal",
    "tier": "Insecticidas y Hormiguicidas",
    "origin": "Nacional"
  },
  {
    "name": "Feit y Olivari",
    "tier": "Fluidos Desinfectantes",
    "origin": "Manchester / Triunfo"
  },
  {
    "name": "Geltex",
    "tier": "Control de Plagas",
    "origin": "Nacional"
  },
  {
    "name": "Ultra",
    "tier": "Raticidas",
    "origin": "Nacional"
  },
  {
    "name": "Prenut",
    "tier": "Granja y Animales de Campo",
    "origin": "Nacional"
  },
  {
    "name": "Semillas & Granos",
    "tier": "Forrajera y Granja",
    "origin": "Nacional"
  },
  {
    "name": "Performance",
    "tier": "Super Premium",
    "origin": "Nacional"
  },
  {
    "name": "The Best / Mi Niño",
    "tier": "Piedras Sanitarias",
    "origin": "Nacional"
  }
]
PRODUCTS_DATA = [
  {
    "id": 1,
    "category_id": 1,
    "brand_id": 5,
    "name": "Dog Chow Adulto Mediana y Grande Triple Proteína",
    "slug": "dog-chow-adulto-mediana-grande",
    "description": "Nutrición balanceada con tecnología ExtraLife y triple fuente de proteína para músculos fuertes y digestión sana.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Más Vendido",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_953311-MLA99349040992_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "20 kg",
        "weight_kg": 20.0,
        "cost_price": 50200.0,
        "margin_percent": 20.0,
        "sale_price": 60240.0,
        "list_price": 69276.0,
        "stock_qty": 50,
        "sku": "DC-AD-MED-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 2,
    "category_id": 1,
    "brand_id": 5,
    "name": "Dog Chow Adulto Mini / Raza Pequeña",
    "slug": "dog-chow-adulto-mini",
    "description": "Croquetas de tamaño adaptado a mandíbulas pequeñas con antioxidantes para una vida larga y saludable.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Raza Pequeña",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_911237-MLA99443772110_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "20 kg",
        "weight_kg": 20.0,
        "cost_price": 53100.0,
        "margin_percent": 20.0,
        "sale_price": 63720.0,
        "list_price": 73278.0,
        "stock_qty": 50,
        "sku": "DC-AD-MINI-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 3,
    "category_id": 1,
    "brand_id": 5,
    "name": "Dog Chow Cachorros Mediana y Grande",
    "slug": "dog-chow-cachorros-mediana-grande",
    "description": "Formulado con DHA para el desarrollo de la visión y cerebro, más calcio para huesos y dientes fuertes.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "grande",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_660096-MLA99920919539_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 57500.0,
        "margin_percent": 20.0,
        "sale_price": 69000.0,
        "list_price": 79350.0,
        "stock_qty": 50,
        "sku": "DC-CACH-MED-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 4,
    "category_id": 1,
    "brand_id": 5,
    "name": "Dog Chow Cachorros Mini / Raza Pequeña",
    "slug": "dog-chow-cachorros-mini",
    "description": "Nutrición concentrada y croquetas pequeñas fáciles de masticar para el primer año de vida de cachorros mini.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "pequeña",
    "badge": "Cachorros Mini",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_660096-MLA99920919539_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 60100.0,
        "margin_percent": 20.0,
        "sale_price": 72120.0,
        "list_price": 82938.0,
        "stock_qty": 50,
        "sku": "DC-CACH-MINI-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 5,
    "category_id": 1,
    "brand_id": 5,
    "name": "Dog Chow Longevidad / Senior 7+",
    "slug": "dog-chow-longevidad-senior",
    "description": "Con glucosamina y prebióticos naturales para mantener la movilidad articular y salud intestinal en perros mayores.",
    "pet_type": "perros",
    "subcat": "senior",
    "breed_size": "todas",
    "badge": "Senior 7+",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_691585-MLA80803318038_112024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 58000.0,
        "margin_percent": 20.0,
        "sale_price": 69600.0,
        "list_price": 80040.0,
        "stock_qty": 50,
        "sku": "DC-SENIOR-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 6,
    "category_id": 2,
    "brand_id": 6,
    "name": "Cat Chow Adulto Delicias de Pescado y Carne",
    "slug": "cat-chow-adulto-pescado-carne",
    "description": "Con Defense Plus: combinación de zinc, selenio y minerales que fortalecen el sistema inmune y tracto urinario.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Clásico Felino",
    "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_825218-MLA99449569190_112025-T.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "8 kg",
        "weight_kg": 8.0,
        "cost_price": 41700.0,
        "margin_percent": 22.0,
        "sale_price": 50874.0,
        "list_price": 58505.0,
        "stock_qty": 50,
        "sku": "CC-FISH-8",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 71700.0,
        "margin_percent": 20.0,
        "sale_price": 86040.0,
        "list_price": 98946.0,
        "stock_qty": 50,
        "sku": "CC-FISH-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 7,
    "category_id": 2,
    "brand_id": 6,
    "name": "Cat Chow Gatitos / Kitten",
    "slug": "cat-chow-gatitos",
    "description": "Con leche materna y DHA para el óptimo desarrollo neurológico y visual en los primeros 12 meses.",
    "pet_type": "gatos",
    "subcat": "gatito",
    "breed_size": "todas",
    "badge": "Gatitos",
    "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_825218-MLA99449569190_112025-T.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 78400.0,
        "margin_percent": 20.0,
        "sale_price": 94080.0,
        "list_price": 108192.0,
        "stock_qty": 50,
        "sku": "CC-KITTEN-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 8,
    "category_id": 1,
    "brand_id": 7,
    "name": "Dogui Perro Adulto Carne, Pollo y Cereales",
    "slug": "dogui-perro-adulto",
    "description": "Alimento completo y económico muy rendidor para perros adultos de todas las razas.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Económico 21 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_944835-MLA99926587971_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 36900.0,
        "margin_percent": 20.0,
        "sale_price": 44280.0,
        "list_price": 50922.0,
        "stock_qty": 50,
        "sku": "DOGUI-AD-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 9,
    "category_id": 1,
    "brand_id": 7,
    "name": "Dogui Cachorros",
    "slug": "dogui-cachorros",
    "description": "Nutrición accesible con proteínas seleccionadas para el crecimiento de cachorros activos.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros 21 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_944835-MLA99926587971_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 40530.0,
        "margin_percent": 20.0,
        "sale_price": 48636.0,
        "list_price": 55931.0,
        "stock_qty": 50,
        "sku": "DOGUI-CACH-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 10,
    "category_id": 2,
    "brand_id": 7,
    "name": "Gati Alimento para Gatos Pescado y Carne",
    "slug": "gati-alimento-gatos",
    "description": "Bolsa familiar de 15 kg muy económica y sabrosa para gatos de todas las edades.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 15 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_660923-MLA99437954454_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 41390.0,
        "margin_percent": 20.0,
        "sale_price": 49668.0,
        "list_price": 57118.0,
        "stock_qty": 50,
        "sku": "GATI-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 11,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Premium Adulto",
    "slug": "dog-selection-premium-adulto",
    "description": "Línea Premium con 23% de proteína noble, extracto de Yucca para reducción de olores y omega 3 y 6.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "mediana",
    "badge": "Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_839215-MLA99350079654_112025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 6600.0,
        "margin_percent": 30.0,
        "sale_price": 8580.0,
        "list_price": 9867.0,
        "stock_qty": 50,
        "sku": "DS-PREM-AD-2",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 37200.0,
        "margin_percent": 20.0,
        "sale_price": 44640.0,
        "list_price": 51336.0,
        "stock_qty": 50,
        "sku": "DS-PREM-AD-15",
        "is_default": 0
      },
      {
        "presentation_name": "21 kg Gigante",
        "weight_kg": 21.0,
        "cost_price": 49000.0,
        "margin_percent": 20.0,
        "sale_price": 58800.0,
        "list_price": 67620.0,
        "stock_qty": 50,
        "sku": "DS-PREM-AD-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 12,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Premium Razas Pequeñas",
    "slug": "dog-selection-premium-razas-pequenas",
    "description": "Croqueta triangular crocante que previene la formación de placa bacteriana en perros pequeños.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Mordida Chica",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_877337-MLA81007028209_112024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 37200.0,
        "margin_percent": 20.0,
        "sale_price": 44640.0,
        "list_price": 51336.0,
        "stock_qty": 50,
        "sku": "DS-PREM-MINI-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 13,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Premium Cachorro",
    "slug": "dog-selection-premium-cachorro",
    "description": "Proteínas de alta biodisponibilidad y balance de calcio-fósforo para el desarrollo musculoesquelético.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_660096-MLA99920919539_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 7800.0,
        "margin_percent": 30.0,
        "sale_price": 10140.0,
        "list_price": 11661.0,
        "stock_qty": 50,
        "sku": "DS-PREM-CACH-2",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 42000.0,
        "margin_percent": 20.0,
        "sale_price": 50400.0,
        "list_price": 57960.0,
        "stock_qty": 50,
        "sku": "DS-PREM-CACH-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 14,
    "category_id": 2,
    "brand_id": 8,
    "name": "Cat Selection Alimento para Gatos Adultos",
    "slug": "cat-selection-adulto",
    "description": "Con pH urinario controlado, taurina esencial y delicioso mix de pescados de mar.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Promo 10+1 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_633625-MLA75145123100_032024-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 12800.0,
        "margin_percent": 25.0,
        "sale_price": 16000.0,
        "list_price": 18400.0,
        "stock_qty": 50,
        "sku": "CAT-SEL-2",
        "is_default": 0
      },
      {
        "presentation_name": "10+1 kg Promo",
        "weight_kg": 11.0,
        "cost_price": 40700.0,
        "margin_percent": 20.0,
        "sale_price": 48840.0,
        "list_price": 56166.0,
        "stock_qty": 50,
        "sku": "CAT-SEL-11",
        "is_default": 1
      }
    ]
  },
  {
    "id": 15,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Criadores Carne y Cereal",
    "slug": "dog-selection-criadores-carne-cereal",
    "description": "Línea profesional para criaderos y familias con varios perros. Excelente rendimiento y heces firmes.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Criadores",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_953311-MLA99349040992_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "1.5 kg",
        "weight_kg": 1.5,
        "cost_price": 4400.0,
        "margin_percent": 30.0,
        "sale_price": 5720.0,
        "list_price": 6578.0,
        "stock_qty": 50,
        "sku": "DS-CRIAD-1.5",
        "is_default": 0
      },
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 8300.0,
        "margin_percent": 25.0,
        "sale_price": 10375.0,
        "list_price": 11931.0,
        "stock_qty": 50,
        "sku": "DS-CRIAD-3",
        "is_default": 0
      },
      {
        "presentation_name": "8 kg",
        "weight_kg": 8.0,
        "cost_price": 18000.0,
        "margin_percent": 22.0,
        "sale_price": 21960.0,
        "list_price": 25254.0,
        "stock_qty": 50,
        "sku": "DS-CRIAD-8",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 31700.0,
        "margin_percent": 20.0,
        "sale_price": 38040.0,
        "list_price": 43746.0,
        "stock_qty": 50,
        "sku": "DS-CRIAD-15",
        "is_default": 0
      },
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 41500.0,
        "margin_percent": 20.0,
        "sale_price": 49800.0,
        "list_price": 57270.0,
        "stock_qty": 50,
        "sku": "DS-CRIAD-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 16,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Criadores Cordero & Arroz (21+3 kg)",
    "slug": "dog-selection-criadores-cordero",
    "description": "¡Edición Especial 21 kg + 3 kg de regalo! Con carne de cordero hipoalergénica para perros con piel sensible.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "21+3 kg Gratis",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_746140-MLA99934028853_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "21+3 kg (24 kg)",
        "weight_kg": 24.0,
        "cost_price": 46600.0,
        "margin_percent": 20.0,
        "sale_price": 55920.0,
        "list_price": 64308.0,
        "stock_qty": 50,
        "sku": "DS-CORD-24",
        "is_default": 1
      }
    ]
  },
  {
    "id": 17,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Criadores Razas Pequeñas",
    "slug": "dog-selection-criadores-razas-pequenas",
    "description": "Fórmula concentrada con mordida pequeña diseñada para el metabolismo activo de perros mini.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Criadores Mini",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_911237-MLA99443772110_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 31700.0,
        "margin_percent": 20.0,
        "sale_price": 38040.0,
        "list_price": 43746.0,
        "stock_qty": 50,
        "sku": "DS-CRIAD-MINI-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 18,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Criadores Cachorros",
    "slug": "dog-selection-criadores-cachorros",
    "description": "Máxima nutrición para camadas en crecimiento con 28% de proteína y aporte balanceado de vitaminas.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_660096-MLA99920919539_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "1.5 kg",
        "weight_kg": 1.5,
        "cost_price": 4900.0,
        "margin_percent": 30.0,
        "sale_price": 6370.0,
        "list_price": 7325.0,
        "stock_qty": 50,
        "sku": "DS-CR-CACH-1.5",
        "is_default": 0
      },
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 9300.0,
        "margin_percent": 25.0,
        "sale_price": 11625.0,
        "list_price": 13369.0,
        "stock_qty": 50,
        "sku": "DS-CR-CACH-3",
        "is_default": 0
      },
      {
        "presentation_name": "8 kg",
        "weight_kg": 8.0,
        "cost_price": 19700.0,
        "margin_percent": 22.0,
        "sale_price": 24034.0,
        "list_price": 27639.0,
        "stock_qty": 50,
        "sku": "DS-CR-CACH-8",
        "is_default": 0
      },
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 46600.0,
        "margin_percent": 20.0,
        "sale_price": 55920.0,
        "list_price": 64308.0,
        "stock_qty": 50,
        "sku": "DS-CR-CACH-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 19,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Criadores Senior & Light",
    "slug": "dog-selection-criadores-senior-light",
    "description": "Bajo en calorías y alto en fibras naturales para el control de peso y cuidado de perros gerontes.",
    "pet_type": "perros",
    "subcat": "senior",
    "breed_size": "todas",
    "badge": "Senior Light",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_691585-MLA80803318038_112024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 35300.0,
        "margin_percent": 20.0,
        "sale_price": 42360.0,
        "list_price": 48714.0,
        "stock_qty": 50,
        "sku": "DS-CR-SENIOR-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 20,
    "category_id": 1,
    "brand_id": 8,
    "name": "Dog Selection Criadores Hipoalergénico",
    "slug": "dog-selection-criadores-hipoalergenico",
    "description": "Mono-proteico sin trigo ni soja, diseñado para perros propensos a alergias cutáneas y digestivas.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Hipoalergénico",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_877337-MLA81007028209_112024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "1.5 kg",
        "weight_kg": 1.5,
        "cost_price": 5300.0,
        "margin_percent": 30.0,
        "sale_price": 6890.0,
        "list_price": 7923.0,
        "stock_qty": 50,
        "sku": "DS-HIPO-1.5",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 37500.0,
        "margin_percent": 20.0,
        "sale_price": 45000.0,
        "list_price": 51750.0,
        "stock_qty": 50,
        "sku": "DS-HIPO-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 21,
    "category_id": 2,
    "brand_id": 8,
    "name": "Loyal Cat Adulto & Gatitos (10+1 kg)",
    "slug": "loyal-cat-adulto-gatitos",
    "description": "Alimento felino sabroso y balanceado con bolsa promocional de 10 kg + 1 kg gratis.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "10+1 kg Promo",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_633625-MLA75145123100_032024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "1 kg",
        "weight_kg": 1.0,
        "cost_price": 1800.0,
        "margin_percent": 35.0,
        "sale_price": 2430.0,
        "list_price": 2794.0,
        "stock_qty": 50,
        "sku": "LOYAL-1",
        "is_default": 0
      },
      {
        "presentation_name": "10+1 kg Promo",
        "weight_kg": 11.0,
        "cost_price": 26800.0,
        "margin_percent": 20.0,
        "sale_price": 32160.0,
        "list_price": 36984.0,
        "stock_qty": 50,
        "sku": "LOYAL-11",
        "is_default": 1
      }
    ]
  },
  {
    "id": 22,
    "category_id": 1,
    "brand_id": 9,
    "name": "DS Etiqueta Negra Adults Derma Care",
    "slug": "ds-etiqueta-negra-adults-derma",
    "description": "Lanzamiento Super Premium: fórmula dermatológica con biotina, zinc y aceite de salmón para piel atópica.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_877337-MLA81007028209_112024-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 8400.0,
        "margin_percent": 25.0,
        "sale_price": 10500.0,
        "list_price": 12075.0,
        "stock_qty": 50,
        "sku": "DSET-DERMA-2",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 47000.0,
        "margin_percent": 20.0,
        "sale_price": 56400.0,
        "list_price": 64860.0,
        "stock_qty": 50,
        "sku": "DSET-DERMA-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 23,
    "category_id": 1,
    "brand_id": 9,
    "name": "DS Etiqueta Negra Adults Razas Medianas y Grandes",
    "slug": "ds-etiqueta-negra-adults-med-large",
    "description": "Proteínas de máxima biodisponibilidad y condroprotectores para articulaciones y vitalidad superior.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_953311-MLA99349040992_112025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 8400.0,
        "margin_percent": 25.0,
        "sale_price": 10500.0,
        "list_price": 12075.0,
        "stock_qty": 50,
        "sku": "DSET-ML-2",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 47000.0,
        "margin_percent": 20.0,
        "sale_price": 56400.0,
        "list_price": 64860.0,
        "stock_qty": 50,
        "sku": "DSET-ML-15",
        "is_default": 0
      },
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 62400.0,
        "margin_percent": 20.0,
        "sale_price": 74880.0,
        "list_price": 86112.0,
        "stock_qty": 50,
        "sku": "DSET-ML-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 24,
    "category_id": 1,
    "brand_id": 9,
    "name": "DS Etiqueta Negra Adults Small Breeds (Razas Pequeñas)",
    "slug": "ds-etiqueta-negra-adults-small-breeds",
    "description": "Croquetas diseñadas para dentaduras pequeñas con complejo prebiótico MOS y FOS.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_911237-MLA99443772110_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 8400.0,
        "margin_percent": 25.0,
        "sale_price": 10500.0,
        "list_price": 12075.0,
        "stock_qty": 50,
        "sku": "DSET-SMALL-2",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 47000.0,
        "margin_percent": 20.0,
        "sale_price": 56400.0,
        "list_price": 64860.0,
        "stock_qty": 50,
        "sku": "DSET-SMALL-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 25,
    "category_id": 1,
    "brand_id": 9,
    "name": "DS Etiqueta Negra Puppies",
    "slug": "ds-etiqueta-negra-puppies",
    "description": "Máxima densidad nutricional y calostro materno para cachorros en sus primeros meses de desarrollo.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_660096-MLA99920919539_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 9100.0,
        "margin_percent": 25.0,
        "sale_price": 11375.0,
        "list_price": 13081.0,
        "stock_qty": 50,
        "sku": "DSET-PUP-2",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 51300.0,
        "margin_percent": 20.0,
        "sale_price": 61560.0,
        "list_price": 70794.0,
        "stock_qty": 50,
        "sku": "DSET-PUP-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 26,
    "category_id": 1,
    "brand_id": 9,
    "name": "DS Etiqueta Negra Senior Light",
    "slug": "ds-etiqueta-negra-senior-light",
    "description": "Soporte cognitivo, glucosamina y L-carnitina para mantener el peso magro en perros adultos mayores.",
    "pet_type": "perros",
    "subcat": "senior",
    "breed_size": "todas",
    "badge": "Senior Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_691585-MLA80803318038_112024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 8400.0,
        "margin_percent": 25.0,
        "sale_price": 10500.0,
        "list_price": 12075.0,
        "stock_qty": 50,
        "sku": "DSET-SENIOR-2",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 47000.0,
        "margin_percent": 20.0,
        "sale_price": 56400.0,
        "list_price": 64860.0,
        "stock_qty": 50,
        "sku": "DSET-SENIOR-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 27,
    "category_id": 2,
    "brand_id": 9,
    "name": "Cat Selection Etiqueta Negra (Adults / Indoor / Kitten / Urinary)",
    "slug": "cat-selection-etiqueta-negra",
    "description": "Línea felina Super Premium con control estricto de bolas de pelo, pH urinario y delicioso salmón.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Super Premium Gatos",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_633625-MLA75145123100_032024-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "2 kg",
        "weight_kg": 2.0,
        "cost_price": 12800.0,
        "margin_percent": 25.0,
        "sale_price": 16000.0,
        "list_price": 18400.0,
        "stock_qty": 50,
        "sku": "CAT-ET-2",
        "is_default": 0
      },
      {
        "presentation_name": "10 kg Adults / Indoor",
        "weight_kg": 10.0,
        "cost_price": 47500.0,
        "margin_percent": 20.0,
        "sale_price": 57000.0,
        "list_price": 65550.0,
        "stock_qty": 50,
        "sku": "CAT-ET-10",
        "is_default": 1
      },
      {
        "presentation_name": "10 kg Kitten",
        "weight_kg": 10.0,
        "cost_price": 48000.0,
        "margin_percent": 20.0,
        "sale_price": 57600.0,
        "list_price": 66240.0,
        "stock_qty": 50,
        "sku": "CAT-ET-KIT-10",
        "is_default": 0
      }
    ]
  },
  {
    "id": 28,
    "category_id": 1,
    "brand_id": 10,
    "name": "Pedigree Adulto Nutrición Completa Carne, Pollo y Vegetales",
    "slug": "pedigree-adulto-nutricion-completa",
    "description": "Alimento balanceado clásico con fibras naturales, omega 6 y zinc para un pelaje reluciente y heces firmes.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Clásico Familiar",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_795475-MLA99878002573_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "8 kg",
        "weight_kg": 8.0,
        "cost_price": 23370.0,
        "margin_percent": 22.0,
        "sale_price": 28511.0,
        "list_price": 32788.0,
        "stock_qty": 50,
        "sku": "PED-8",
        "is_default": 0
      },
      {
        "presentation_name": "21 kg Gigante",
        "weight_kg": 21.0,
        "cost_price": 52390.0,
        "margin_percent": 20.0,
        "sale_price": 62868.0,
        "list_price": 72298.0,
        "stock_qty": 50,
        "sku": "PED-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 29,
    "category_id": 1,
    "brand_id": 10,
    "name": "Pedigree Cachorros Sano Crecimiento",
    "slug": "pedigree-cachorros-sano-crecimiento",
    "description": "Con prebióticos y DHA para el óptimo aprendizaje y refuerzo de las defensas naturales del cachorro.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros 21 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_704334-MLA99335499802_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 55490.0,
        "margin_percent": 20.0,
        "sale_price": 66588.0,
        "list_price": 76576.0,
        "stock_qty": 50,
        "sku": "PED-CACH-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 30,
    "category_id": 1,
    "brand_id": 10,
    "name": "Pedigree Adulto Salmón o Cordero",
    "slug": "pedigree-adulto-salmon-cordero",
    "description": "Variedad deliciosa con carnes selectas para consentir el paladar de tu perro adulto.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 21 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_795475-MLA99878002573_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "21 kg",
        "weight_kg": 21.0,
        "cost_price": 52390.0,
        "margin_percent": 20.0,
        "sale_price": 62868.0,
        "list_price": 72298.0,
        "stock_qty": 50,
        "sku": "PED-SALM-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 31,
    "category_id": 1,
    "brand_id": 10,
    "name": "Pedigree Senior 7+",
    "slug": "pedigree-senior-7",
    "description": "Fácil digestión y bocados más suaves adaptados a las encías y salud de perros senior.",
    "pet_type": "perros",
    "subcat": "senior",
    "breed_size": "todas",
    "badge": "Senior 9 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_691585-MLA80803318038_112024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "9 kg",
        "weight_kg": 9.0,
        "cost_price": 21120.0,
        "margin_percent": 22.0,
        "sale_price": 25766.0,
        "list_price": 29631.0,
        "stock_qty": 50,
        "sku": "PED-SENIOR-9",
        "is_default": 1
      }
    ]
  },
  {
    "id": 32,
    "category_id": 2,
    "brand_id": 11,
    "name": "Whiskas Gato Adulto Carne, Pollo o Pescado",
    "slug": "whiskas-gato-adulto",
    "description": "Nuggets crujientes rellenos con crema de carne o pescado. Minerales balanceados para vías urinarias sanas.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Más Elegido",
    "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_851344-MLA110627789901_042026-T.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "10 kg",
        "weight_kg": 10.0,
        "cost_price": 40900.0,
        "margin_percent": 20.0,
        "sale_price": 49080.0,
        "list_price": 56442.0,
        "stock_qty": 50,
        "sku": "WHISK-10",
        "is_default": 0
      },
      {
        "presentation_name": "20 kg Gigante",
        "weight_kg": 20.0,
        "cost_price": 71450.0,
        "margin_percent": 20.0,
        "sale_price": 85740.0,
        "list_price": 98601.0,
        "stock_qty": 50,
        "sku": "WHISK-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 33,
    "category_id": 2,
    "brand_id": 11,
    "name": "Whiskas Gato Castrados & Salmón",
    "slug": "whiskas-castrados-salmon",
    "description": "Control calórico y aporte justo de fibras para evitar el aumento de peso en felinos esterilizados.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Castrados 10 kg",
    "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_851344-MLA110627789901_042026-T.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "10 kg",
        "weight_kg": 10.0,
        "cost_price": 45770.0,
        "margin_percent": 20.0,
        "sale_price": 54924.0,
        "list_price": 63163.0,
        "stock_qty": 50,
        "sku": "WHISK-CAST-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 34,
    "category_id": 1,
    "brand_id": 10,
    "name": "Pedigree & Whiskas Latas Alimento Húmedo",
    "slug": "latas-pedigree-whiskas",
    "description": "Deliciosos trozos de carne y pollo en salsa suculenta. Hidratación y palatabilidad irresistible.",
    "pet_type": "ambos",
    "subcat": "humedo",
    "breed_size": "todas",
    "badge": "Lata Individual",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_876741-MLU79111404727_092024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Lata 290g / 340g",
        "weight_kg": 0.34,
        "cost_price": 3220.0,
        "margin_percent": 30.0,
        "sale_price": 4186.0,
        "list_price": 4814.0,
        "stock_qty": 50,
        "sku": "LATA-PW-1",
        "is_default": 1
      }
    ]
  },
  {
    "id": 35,
    "category_id": 1,
    "brand_id": 10,
    "name": "Pedigree & Whiskas Pouch Caja x 10 Sobres + 2 Gratis",
    "slug": "pouch-caja-10-mas-2",
    "description": "¡Caja ahorro con 10 sobres + 2 de regalo! El alimento húmedo favorito de perros y gatos para mezclar con el alimento seco.",
    "pet_type": "ambos",
    "subcat": "humedo",
    "breed_size": "todas",
    "badge": "10+2 Regalo",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_876741-MLU79111404727_092024-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Caja 12 sobres",
        "weight_kg": 1.0,
        "cost_price": 11200.0,
        "margin_percent": 25.0,
        "sale_price": 14000.0,
        "list_price": 16100.0,
        "stock_qty": 50,
        "sku": "POUCH-CAJA-12",
        "is_default": 1
      }
    ]
  },
  {
    "id": 36,
    "category_id": 3,
    "brand_id": 11,
    "name": "Whiskas Snacks Rellenos para Gato",
    "slug": "whiskas-snacks-rellenos",
    "description": "Golosinas crujientes por fuera con relleno cremoso irresistible de salmón, pollo o carne.",
    "pet_type": "gatos",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "Golosina Gatos",
    "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_851344-MLA110627789901_042026-T.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Sobre 40 g",
        "weight_kg": 0.04,
        "cost_price": 1320.0,
        "margin_percent": 35.0,
        "sale_price": 1782.0,
        "list_price": 2049.0,
        "stock_qty": 50,
        "sku": "WHISK-SNACK-40",
        "is_default": 0
      },
      {
        "presentation_name": "Sobre 80 g",
        "weight_kg": 0.08,
        "cost_price": 2220.0,
        "margin_percent": 35.0,
        "sale_price": 2997.0,
        "list_price": 3447.0,
        "stock_qty": 50,
        "sku": "WHISK-SNACK-80",
        "is_default": 1
      }
    ]
  },
  {
    "id": 37,
    "category_id": 3,
    "brand_id": 10,
    "name": "Pedigree Tasty Bites Carne / Pollo",
    "slug": "pedigree-tasty-bites",
    "description": "Bocaditos tiernos y jugosos con carne real para premiar a tu perro en el adiestramiento o paseo.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "Premios Tiernos",
    "image_url": "https://resources.claroshop.com/medios-plazavip/mkt/646d0036c12bf_6jpg.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Pack 40 g",
        "weight_kg": 0.04,
        "cost_price": 1050.0,
        "margin_percent": 35.0,
        "sale_price": 1418.0,
        "list_price": 1631.0,
        "stock_qty": 50,
        "sku": "TASTY-40",
        "is_default": 0
      },
      {
        "presentation_name": "Pack 80 g",
        "weight_kg": 0.08,
        "cost_price": 1780.0,
        "margin_percent": 35.0,
        "sale_price": 2403.0,
        "list_price": 2763.0,
        "stock_qty": 50,
        "sku": "TASTY-80",
        "is_default": 1
      }
    ]
  },
  {
    "id": 38,
    "category_id": 3,
    "brand_id": 12,
    "name": "Temptations Snacks Crujientes para Gatos",
    "slug": "temptations-snacks-gato",
    "description": "¡El snack felino número 1 del mundo! Pollo, atún o salmón con menos de 2 calorías por bocado.",
    "pet_type": "gatos",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "Snack Felino #1",
    "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_851344-MLA110627789901_042026-T.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Pack 48 g",
        "weight_kg": 0.048,
        "cost_price": 2770.0,
        "margin_percent": 35.0,
        "sale_price": 3740.0,
        "list_price": 4301.0,
        "stock_qty": 50,
        "sku": "TEMPT-48",
        "is_default": 1
      }
    ]
  },
  {
    "id": 39,
    "category_id": 3,
    "brand_id": 13,
    "name": "Dentastix Cuidado Dental Diario Razas Pequeñas",
    "slug": "dentastix-raza-pequena",
    "description": "Barra dental en forma de X clinicamente comprobada para reducir hasta un 80% la acumulación de sarro.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "pequeña",
    "badge": "Salud Dental",
    "image_url": "https://resources.claroshop.com/medios-plazavip/mkt/646d0036c12bf_6jpg.jpg",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "1 Unidad",
        "weight_kg": 0.03,
        "cost_price": 430.0,
        "margin_percent": 35.0,
        "sale_price": 580.0,
        "list_price": 667.0,
        "stock_qty": 50,
        "sku": "DENT-MINI-1",
        "is_default": 0
      },
      {
        "presentation_name": "Pack x 3 Unidades",
        "weight_kg": 0.09,
        "cost_price": 1250.0,
        "margin_percent": 35.0,
        "sale_price": 1688.0,
        "list_price": 1941.0,
        "stock_qty": 50,
        "sku": "DENT-MINI-3",
        "is_default": 0
      },
      {
        "presentation_name": "Pack Semanal x 7 Unid.",
        "weight_kg": 0.21,
        "cost_price": 2420.0,
        "margin_percent": 30.0,
        "sale_price": 3146.0,
        "list_price": 3618.0,
        "stock_qty": 50,
        "sku": "DENT-MINI-7",
        "is_default": 1
      }
    ]
  },
  {
    "id": 40,
    "category_id": 3,
    "brand_id": 13,
    "name": "Dentastix Cuidado Dental Diario Razas Medianas y Grandes",
    "slug": "dentastix-raza-mediana",
    "description": "Cuidado bucal integral para perros de más de 10 kg. Limpia los dientes difíciles y combate el mal aliento.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "grande",
    "badge": "Salud Dental",
    "image_url": "https://resources.claroshop.com/medios-plazavip/mkt/646d0036c12bf_6jpg.jpg",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "1 Unidad",
        "weight_kg": 0.05,
        "cost_price": 510.0,
        "margin_percent": 35.0,
        "sale_price": 688.0,
        "list_price": 791.0,
        "stock_qty": 50,
        "sku": "DENT-MED-1",
        "is_default": 0
      },
      {
        "presentation_name": "Pack x 3 Unidades",
        "weight_kg": 0.15,
        "cost_price": 1450.0,
        "margin_percent": 35.0,
        "sale_price": 1958.0,
        "list_price": 2252.0,
        "stock_qty": 50,
        "sku": "DENT-MED-3",
        "is_default": 0
      },
      {
        "presentation_name": "Pack Semanal x 7 Unid.",
        "weight_kg": 0.35,
        "cost_price": 2850.0,
        "margin_percent": 30.0,
        "sale_price": 3705.0,
        "list_price": 4261.0,
        "stock_qty": 50,
        "sku": "DENT-MED-7",
        "is_default": 1
      }
    ]
  },
  {
    "id": 41,
    "category_id": 3,
    "brand_id": 14,
    "name": "Biscrok Multi Galletitas Crocantes para Perro",
    "slug": "biscrok-multi-galletitas",
    "description": "Huesitos horneados crocantes de tres sabores con calcio y minerales para premiar a tu mejor amigo.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "Galletitas",
    "image_url": "https://resources.claroshop.com/medios-plazavip/mkt/646d0036c12bf_6jpg.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Caja 100 g",
        "weight_kg": 0.1,
        "cost_price": 1430.0,
        "margin_percent": 35.0,
        "sale_price": 1931.0,
        "list_price": 2221.0,
        "stock_qty": 50,
        "sku": "BISC-100",
        "is_default": 0
      },
      {
        "presentation_name": "Caja Familiar 500 g",
        "weight_kg": 0.5,
        "cost_price": 4590.0,
        "margin_percent": 30.0,
        "sale_price": 5967.0,
        "list_price": 6862.0,
        "stock_qty": 50,
        "sku": "BISC-500",
        "is_default": 1
      }
    ]
  },
  {
    "id": 42,
    "category_id": 1,
    "brand_id": 2,
    "name": "Pro Plan Adulto Raza Pequeña (OptiHealth)",
    "slug": "pro-plan-adulto-raza-pequena",
    "description": "Carne fresca de pollo como 1° ingrediente con espirulina para proteger el sistema inmune de perros pequeños.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_913729-MLA99843470895_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 31150.0,
        "margin_percent": 22.0,
        "sale_price": 38003.0,
        "list_price": 43703.0,
        "stock_qty": 50,
        "sku": "PP-AD-MINI-3",
        "is_default": 0
      },
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 63780.0,
        "margin_percent": 20.0,
        "sale_price": 76536.0,
        "list_price": 88016.0,
        "stock_qty": 50,
        "sku": "PP-AD-MINI-7.5",
        "is_default": 1
      }
    ]
  },
  {
    "id": 43,
    "category_id": 1,
    "brand_id": 2,
    "name": "Pro Plan Adulto Raza Mediana y Grande",
    "slug": "pro-plan-adulto-raza-mediana-grande",
    "description": "Nutrición avanzada con proteína de alta calidad y ácidos grasos esenciales para articulaciones y masa magra.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_913729-MLA99843470895_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 30090.0,
        "margin_percent": 22.0,
        "sale_price": 36710.0,
        "list_price": 42216.0,
        "stock_qty": 50,
        "sku": "PP-AD-MED-3",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 100690.0,
        "margin_percent": 20.0,
        "sale_price": 120828.0,
        "list_price": 138952.0,
        "stock_qty": 50,
        "sku": "PP-AD-MED-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 44,
    "category_id": 1,
    "brand_id": 2,
    "name": "Pro Plan Puppy Raza Pequeña (OptiStart)",
    "slug": "pro-plan-puppy-raza-pequena",
    "description": "Formulado con anticuerpos naturales del calostro bovino para extender la protección materna en cachorros mini.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "pequeña",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_913729-MLA99843470895_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 34200.0,
        "margin_percent": 22.0,
        "sale_price": 41724.0,
        "list_price": 47983.0,
        "stock_qty": 50,
        "sku": "PP-PUP-MINI-3",
        "is_default": 0
      },
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 70650.0,
        "margin_percent": 20.0,
        "sale_price": 84780.0,
        "list_price": 97497.0,
        "stock_qty": 50,
        "sku": "PP-PUP-MINI-7.5",
        "is_default": 1
      }
    ]
  },
  {
    "id": 45,
    "category_id": 1,
    "brand_id": 2,
    "name": "Pro Plan Puppy Raza Mediana y Grande",
    "slug": "pro-plan-puppy-raza-mediana-grande",
    "description": "Óptima relación calcio/fósforo y DHA para un desarrollo esquelético y articular armonioso en cachorros grandes.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "grande",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_913729-MLA99843470895_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 32850.0,
        "margin_percent": 22.0,
        "sale_price": 40077.0,
        "list_price": 46089.0,
        "stock_qty": 50,
        "sku": "PP-PUP-MED-3",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 110790.0,
        "margin_percent": 20.0,
        "sale_price": 132948.0,
        "list_price": 152890.0,
        "stock_qty": 50,
        "sku": "PP-PUP-MED-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 46,
    "category_id": 1,
    "brand_id": 2,
    "name": "Pro Plan Reduce Calorie Mediana y Grande",
    "slug": "pro-plan-reduce-calorie",
    "description": "Con 20% menos de calorías y alto tenor de fibra para facilitar la pérdida de peso corporal sin perder masa muscular.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Control de Peso",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_913729-MLA99843470895_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "12 kg",
        "weight_kg": 12.0,
        "cost_price": 96370.0,
        "margin_percent": 20.0,
        "sale_price": 115644.0,
        "list_price": 132991.0,
        "stock_qty": 50,
        "sku": "PP-LIGHT-12",
        "is_default": 1
      }
    ]
  },
  {
    "id": 47,
    "category_id": 2,
    "brand_id": 2,
    "name": "Pro Plan Cat Adulto Salmón (OptiRenal)",
    "slug": "pro-plan-cat-adulto",
    "description": "Tecnología OptiRenal que protege la función renal a lo largo de toda la vida adulta del felino.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Salud Renal",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_913729-MLA99843470895_112025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "1 kg",
        "weight_kg": 1.0,
        "cost_price": 15550.0,
        "margin_percent": 25.0,
        "sale_price": 19438.0,
        "list_price": 22354.0,
        "stock_qty": 50,
        "sku": "PP-CAT-1",
        "is_default": 0
      },
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 85460.0,
        "margin_percent": 20.0,
        "sale_price": 102552.0,
        "list_price": 117935.0,
        "stock_qty": 50,
        "sku": "PP-CAT-7.5",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 150030.0,
        "margin_percent": 20.0,
        "sale_price": 180036.0,
        "list_price": 207041.0,
        "stock_qty": 50,
        "sku": "PP-CAT-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 48,
    "category_id": 2,
    "brand_id": 2,
    "name": "Pro Plan Cat Urinary Care",
    "slug": "pro-plan-cat-urinary",
    "description": "Fórmula especializada que acidifica levemente la orina y disuelve cálculos de estruvita en gatos propensos.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Veterinaria Felina",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_913729-MLA99843470895_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 93820.0,
        "margin_percent": 20.0,
        "sale_price": 112584.0,
        "list_price": 129472.0,
        "stock_qty": 50,
        "sku": "PP-CAT-URIN-7.5",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 160480.0,
        "margin_percent": 20.0,
        "sale_price": 192576.0,
        "list_price": 221462.0,
        "stock_qty": 50,
        "sku": "PP-CAT-URIN-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 49,
    "category_id": 1,
    "brand_id": 1,
    "name": "Royal Canin Mini Adulto",
    "slug": "royal-canin-mini-adulto",
    "description": "Nutrición a medida para perros adultos de raza pequeña (hasta 10 kg). Mantiene el peso ideal y salud del pelaje.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Super Premium",
    "image_url": "https://catycanar.vtexassets.com/arquivos/ids/177185-800-auto?v=639214509443130000&width=800&height=auto&aspect=true",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 35400.0,
        "margin_percent": 22.0,
        "sale_price": 43188.0,
        "list_price": 49666.0,
        "stock_qty": 50,
        "sku": "RC-MINI-3",
        "is_default": 0
      },
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 81170.0,
        "margin_percent": 20.0,
        "sale_price": 97404.0,
        "list_price": 112015.0,
        "stock_qty": 50,
        "sku": "RC-MINI-7.5",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg Nuevo",
        "weight_kg": 15.0,
        "cost_price": 133460.0,
        "margin_percent": 20.0,
        "sale_price": 160152.0,
        "list_price": 184175.0,
        "stock_qty": 50,
        "sku": "RC-MINI-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 50,
    "category_id": 1,
    "brand_id": 1,
    "name": "Royal Canin Mini Puppy / Junior",
    "slug": "royal-canin-mini-puppy",
    "description": "Para cachorros de razas pequeñas hasta los 10 meses. Refuerza las defensas naturales y apoya el crecimiento equilibrado.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "pequeña",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_877136-MLA99395424832_112025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 36900.0,
        "margin_percent": 22.0,
        "sale_price": 45018.0,
        "list_price": 51771.0,
        "stock_qty": 50,
        "sku": "RC-PUP-3",
        "is_default": 0
      },
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 74340.0,
        "margin_percent": 20.0,
        "sale_price": 89208.0,
        "list_price": 102589.0,
        "stock_qty": 50,
        "sku": "RC-PUP-7.5",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 138290.0,
        "margin_percent": 20.0,
        "sale_price": 165948.0,
        "list_price": 190840.0,
        "stock_qty": 50,
        "sku": "RC-PUP-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 51,
    "category_id": 1,
    "brand_id": 1,
    "name": "Royal Canin Medium Adulto & Junior",
    "slug": "royal-canin-medium",
    "description": "Para perros adultos de 11 a 25 kg. Promueve una alta digestibilidad y refuerza la barrera natural de la piel.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "mediana",
    "badge": "Super Premium",
    "image_url": "https://catycanar.vtexassets.com/arquivos/ids/177185-800-auto?v=639214509443130000&width=800&height=auto&aspect=true",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Medium Adulto 15 kg",
        "weight_kg": 15.0,
        "cost_price": 126000.0,
        "margin_percent": 20.0,
        "sale_price": 151200.0,
        "list_price": 173880.0,
        "stock_qty": 50,
        "sku": "RC-MED-AD-15",
        "is_default": 1
      },
      {
        "presentation_name": "Medium Junior 15 kg",
        "weight_kg": 15.0,
        "cost_price": 134700.0,
        "margin_percent": 20.0,
        "sale_price": 161640.0,
        "list_price": 185886.0,
        "stock_qty": 50,
        "sku": "RC-MED-JR-15",
        "is_default": 0
      }
    ]
  },
  {
    "id": 52,
    "category_id": 1,
    "brand_id": 1,
    "name": "Royal Canin Maxi Adulto & Junior",
    "slug": "royal-canin-maxi",
    "description": "Diseñado para perros grandes (26 a 44 kg). Soporte osteoarticular reforzado con glucosamina y EPA-DHA.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Razas Grandes",
    "image_url": "https://catycanar.vtexassets.com/arquivos/ids/177185-800-auto?v=639214509443130000&width=800&height=auto&aspect=true",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Maxi Adulto 15 kg",
        "weight_kg": 15.0,
        "cost_price": 126100.0,
        "margin_percent": 20.0,
        "sale_price": 151320.0,
        "list_price": 174018.0,
        "stock_qty": 50,
        "sku": "RC-MAXI-AD-15",
        "is_default": 1
      },
      {
        "presentation_name": "Maxi Junior 15 kg",
        "weight_kg": 15.0,
        "cost_price": 134700.0,
        "margin_percent": 20.0,
        "sale_price": 161640.0,
        "list_price": 185886.0,
        "stock_qty": 50,
        "sku": "RC-MAXI-JR-15",
        "is_default": 0
      }
    ]
  },
  {
    "id": 53,
    "category_id": 1,
    "brand_id": 1,
    "name": "Royal Canin Específico Razas (Caniche, Bulldog, Yorkshire)",
    "slug": "royal-canin-especifico-razas",
    "description": "Croqueta y nutrición formulada específicamente para las necesidades anatómicas y genéticas de cada raza.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Especial Razas",
    "image_url": "https://catycanar.vtexassets.com/arquivos/ids/177185-800-auto?v=639214509443130000&width=800&height=auto&aspect=true",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Caniche Adulto 3 kg",
        "weight_kg": 3.0,
        "cost_price": 38600.0,
        "margin_percent": 22.0,
        "sale_price": 47092.0,
        "list_price": 54156.0,
        "stock_qty": 50,
        "sku": "RC-CANICHE-3",
        "is_default": 1
      },
      {
        "presentation_name": "Bulldog Francés 3 kg",
        "weight_kg": 3.0,
        "cost_price": 38600.0,
        "margin_percent": 22.0,
        "sale_price": 47092.0,
        "list_price": 54156.0,
        "stock_qty": 50,
        "sku": "RC-BULLDOG-3",
        "is_default": 0
      },
      {
        "presentation_name": "Yorkshire Terrier 3 kg",
        "weight_kg": 3.0,
        "cost_price": 38600.0,
        "margin_percent": 22.0,
        "sale_price": 47092.0,
        "list_price": 54156.0,
        "stock_qty": 50,
        "sku": "RC-YORK-3",
        "is_default": 0
      }
    ]
  },
  {
    "id": 54,
    "category_id": 2,
    "brand_id": 1,
    "name": "Royal Canin Gato Fit 32",
    "slug": "royal-canin-gato-fit-32",
    "description": "Alimento completo para gatos adultos con actividad física moderada. Favorece la eliminación de bolas de pelo.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Más Vendido Gatos",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_615731-MLA100085791445_122025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "1.5 kg",
        "weight_kg": 1.5,
        "cost_price": 26350.0,
        "margin_percent": 25.0,
        "sale_price": 32938.0,
        "list_price": 37879.0,
        "stock_qty": 50,
        "sku": "RC-FIT-1.5",
        "is_default": 0
      },
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 110750.0,
        "margin_percent": 20.0,
        "sale_price": 132900.0,
        "list_price": 152835.0,
        "stock_qty": 50,
        "sku": "RC-FIT-7.5",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 186750.0,
        "margin_percent": 20.0,
        "sale_price": 224100.0,
        "list_price": 257715.0,
        "stock_qty": 50,
        "sku": "RC-FIT-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 55,
    "category_id": 2,
    "brand_id": 1,
    "name": "Royal Canin Gato Castrado / Sterilised",
    "slug": "royal-canin-gato-castrado",
    "description": "Nutrición precisa para controlar el aumento de peso y cuidar la salud del tracto urinario en felinos castrados.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Castrados",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_615731-MLA100085791445_122025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 110420.0,
        "margin_percent": 20.0,
        "sale_price": 132504.0,
        "list_price": 152380.0,
        "stock_qty": 50,
        "sku": "RC-CASTR-7.5",
        "is_default": 1
      }
    ]
  },
  {
    "id": 56,
    "category_id": 1,
    "brand_id": 15,
    "name": "Excellent Perro Adulto Raza Pequeña",
    "slug": "excellent-perro-adulto-raza-pequena",
    "description": "Con Smart Nutrition System: proteínas de pollo y arroz para máxima digestibilidad en perros mini.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_816176-MLA99341181006_112025-F.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 63200.0,
        "margin_percent": 20.0,
        "sale_price": 75840.0,
        "list_price": 87216.0,
        "stock_qty": 50,
        "sku": "EXC-MINI-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 57,
    "category_id": 1,
    "brand_id": 15,
    "name": "Excellent Perro Adulto Mediana y Grande",
    "slug": "excellent-perro-adulto-mediana-grande",
    "description": "Equilibrio óptimo de nutrientes para perros de porte mediano y grande, manteniendo vitalidad y masa magra.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_816176-MLA99341181006_112025-F.jpg",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 60300.0,
        "margin_percent": 20.0,
        "sale_price": 72360.0,
        "list_price": 83214.0,
        "stock_qty": 50,
        "sku": "EXC-MED-15",
        "is_default": 0
      },
      {
        "presentation_name": "20 kg Gigante",
        "weight_kg": 20.0,
        "cost_price": 71600.0,
        "margin_percent": 20.0,
        "sale_price": 85920.0,
        "list_price": 98808.0,
        "stock_qty": 50,
        "sku": "EXC-MED-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 58,
    "category_id": 2,
    "brand_id": 15,
    "name": "Excellent Cat Adulto Pollo y Arroz",
    "slug": "excellent-cat-adulto",
    "description": "Fórmula altamente palatable con taurina y metionina para mantener un corazón y vista fuertes en gatos.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Calidad Purina",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_816176-MLA99341181006_112025-F.jpg",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "3 kg",
        "weight_kg": 3.0,
        "cost_price": 26500.0,
        "margin_percent": 22.0,
        "sale_price": 32330.0,
        "list_price": 37180.0,
        "stock_qty": 50,
        "sku": "EXC-CAT-3",
        "is_default": 0
      },
      {
        "presentation_name": "7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 54200.0,
        "margin_percent": 20.0,
        "sale_price": 65040.0,
        "list_price": 74796.0,
        "stock_qty": 50,
        "sku": "EXC-CAT-7.5",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 104500.0,
        "margin_percent": 20.0,
        "sale_price": 125400.0,
        "list_price": 144210.0,
        "stock_qty": 50,
        "sku": "EXC-CAT-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 59,
    "category_id": 1,
    "brand_id": 16,
    "name": "Vital Can Balanced Perro Adulto",
    "slug": "vital-can-balanced-perro-adulto",
    "description": "Línea Balanced con moderación calórica y extracto de Yucca para disminuir sensiblemente los olores de las heces.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Industria Nacional",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_678554-MLA99451664162_112025-F.jpg",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Raza Pequeña 15 kg",
        "weight_kg": 15.0,
        "cost_price": 51400.0,
        "margin_percent": 20.0,
        "sale_price": 61680.0,
        "list_price": 70932.0,
        "stock_qty": 50,
        "sku": "VC-BAL-MINI-15",
        "is_default": 0
      },
      {
        "presentation_name": "Raza Med/Grande 20 kg",
        "weight_kg": 20.0,
        "cost_price": 63900.0,
        "margin_percent": 20.0,
        "sale_price": 76680.0,
        "list_price": 88182.0,
        "stock_qty": 50,
        "sku": "VC-BAL-MED-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 60,
    "category_id": 1,
    "brand_id": 16,
    "name": "Vital Can Balanced Cachorro",
    "slug": "vital-can-balanced-cachorro",
    "description": "Con DHA y proteínas lácteas para un crecimiento armónico de cachorros en sus primeros 12 meses.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_678554-MLA99451664162_112025-F.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Raza Pequeña 7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 38700.0,
        "margin_percent": 22.0,
        "sale_price": 47214.0,
        "list_price": 54296.0,
        "stock_qty": 50,
        "sku": "VC-BAL-CACH-7.5",
        "is_default": 0
      },
      {
        "presentation_name": "Raza Med/Grande 20 kg",
        "weight_kg": 20.0,
        "cost_price": 78400.0,
        "margin_percent": 20.0,
        "sale_price": 94080.0,
        "list_price": 108192.0,
        "stock_qty": 50,
        "sku": "VC-BAL-CACH-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 61,
    "category_id": 1,
    "brand_id": 16,
    "name": "Vital Can Complete Adulto & Cachorro",
    "slug": "vital-can-complete",
    "description": "Línea Complete familiar de gran sabor con cereales nobles y vitaminas esenciales para perros activos.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 20 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_678554-MLA99451664162_112025-F.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Complete Adulto 20 kg",
        "weight_kg": 20.0,
        "cost_price": 48100.0,
        "margin_percent": 20.0,
        "sale_price": 57720.0,
        "list_price": 66378.0,
        "stock_qty": 50,
        "sku": "VC-COMP-AD-20",
        "is_default": 1
      },
      {
        "presentation_name": "Complete Cachorro 20 kg",
        "weight_kg": 20.0,
        "cost_price": 53000.0,
        "margin_percent": 20.0,
        "sale_price": 63600.0,
        "list_price": 73140.0,
        "stock_qty": 50,
        "sku": "VC-COMP-CACH-20",
        "is_default": 0
      }
    ]
  },
  {
    "id": 62,
    "category_id": 1,
    "brand_id": 3,
    "name": "Eukanuba Adulto Razas Pequeñas, Medianas y Grandes",
    "slug": "eukanuba-adulto",
    "description": "Proteína de origen animal de alta calidad con sistema dental DentaDefense 3D para reducir sarro.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Super Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_832243-MLA99340263690_112025-F.jpg",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Small Breed 3 kg",
        "weight_kg": 3.0,
        "cost_price": 21500.0,
        "margin_percent": 22.0,
        "sale_price": 26230.0,
        "list_price": 30164.0,
        "stock_qty": 50,
        "sku": "EUK-SMALL-3",
        "is_default": 0
      },
      {
        "presentation_name": "Small Breed 15 kg",
        "weight_kg": 15.0,
        "cost_price": 83100.0,
        "margin_percent": 20.0,
        "sale_price": 99720.0,
        "list_price": 114678.0,
        "stock_qty": 50,
        "sku": "EUK-SMALL-15",
        "is_default": 1
      },
      {
        "presentation_name": "Medium Breed 15 kg",
        "weight_kg": 15.0,
        "cost_price": 80600.0,
        "margin_percent": 20.0,
        "sale_price": 96720.0,
        "list_price": 111228.0,
        "stock_qty": 50,
        "sku": "EUK-MED-15",
        "is_default": 0
      },
      {
        "presentation_name": "Large Breed 15 kg",
        "weight_kg": 15.0,
        "cost_price": 80300.0,
        "margin_percent": 20.0,
        "sale_price": 96360.0,
        "list_price": 110814.0,
        "stock_qty": 50,
        "sku": "EUK-LRG-15",
        "is_default": 0
      }
    ]
  },
  {
    "id": 63,
    "category_id": 1,
    "brand_id": 3,
    "name": "Eukanuba Puppy Cachorro",
    "slug": "eukanuba-puppy",
    "description": "Niveles clínicamente comprobados de DHA para cachorros más inteligentes y fáciles de entrenar.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_832243-MLA99340263690_112025-F.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Puppy Small 3 kg",
        "weight_kg": 3.0,
        "cost_price": 22400.0,
        "margin_percent": 22.0,
        "sale_price": 27328.0,
        "list_price": 31427.0,
        "stock_qty": 50,
        "sku": "EUK-PUP-SM-3",
        "is_default": 0
      },
      {
        "presentation_name": "Puppy Small 15 kg",
        "weight_kg": 15.0,
        "cost_price": 85300.0,
        "margin_percent": 20.0,
        "sale_price": 102360.0,
        "list_price": 117714.0,
        "stock_qty": 50,
        "sku": "EUK-PUP-SM-15",
        "is_default": 1
      },
      {
        "presentation_name": "Puppy Medium 15 kg",
        "weight_kg": 15.0,
        "cost_price": 80900.0,
        "margin_percent": 20.0,
        "sale_price": 97080.0,
        "list_price": 111642.0,
        "stock_qty": 50,
        "sku": "EUK-PUP-MED-15",
        "is_default": 0
      }
    ]
  },
  {
    "id": 64,
    "category_id": 1,
    "brand_id": 4,
    "name": "Sieger Adulto Mordida Pequeña, Mediana y Grande",
    "slug": "sieger-adulto",
    "description": "Nutrición premium nacional de vanguardia con condroprotectores, glucosamina y ácidos omega 3 y 6.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Más Recomendado",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_615731-MLA100085791445_122025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Mini Adulto 12 kg",
        "weight_kg": 12.0,
        "cost_price": 63400.0,
        "margin_percent": 20.0,
        "sale_price": 76080.0,
        "list_price": 87492.0,
        "stock_qty": 50,
        "sku": "SG-MINI-12",
        "is_default": 0
      },
      {
        "presentation_name": "Med & Large 15 kg",
        "weight_kg": 15.0,
        "cost_price": 72800.0,
        "margin_percent": 20.0,
        "sale_price": 87360.0,
        "list_price": 100464.0,
        "stock_qty": 50,
        "sku": "SG-MED-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 65,
    "category_id": 1,
    "brand_id": 4,
    "name": "Sieger Puppy Cachorros Mini & Med/Large",
    "slug": "sieger-puppy",
    "description": "Desarrollo osteoarticular superior y máxima digestibilidad para cachorros exigentes.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_615731-MLA100085791445_122025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Puppy Mini 12 kg",
        "weight_kg": 12.0,
        "cost_price": 68000.0,
        "margin_percent": 20.0,
        "sale_price": 81600.0,
        "list_price": 93840.0,
        "stock_qty": 50,
        "sku": "SG-PUP-MINI-12",
        "is_default": 0
      },
      {
        "presentation_name": "Puppy Med & Large 15 kg",
        "weight_kg": 15.0,
        "cost_price": 77330.0,
        "margin_percent": 20.0,
        "sale_price": 92796.0,
        "list_price": 106715.0,
        "stock_qty": 50,
        "sku": "SG-PUP-MED-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 66,
    "category_id": 1,
    "brand_id": 4,
    "name": "Sieger Criadores All in One (20 kg)",
    "slug": "sieger-criadores-all-in-one",
    "description": "Fórmula de alto rendimiento profesional para criadores con 28% de proteína y alta densidad calórica.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Criadores 20 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_816176-MLA99341181006_112025-F.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "20 kg All in One",
        "weight_kg": 20.0,
        "cost_price": 77700.0,
        "margin_percent": 20.0,
        "sale_price": 93240.0,
        "list_price": 107226.0,
        "stock_qty": 50,
        "sku": "SG-ALLINONE-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 67,
    "category_id": 1,
    "brand_id": 25,
    "name": "Agility Perro Adulto y Cachorros",
    "slug": "agility-perro",
    "description": "Alimento balanceado con proteínas seleccionadas y pulpa de remolacha para una óptima asimilación intestinal.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Línea Sieger",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_615731-MLA100085791445_122025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Talla Pequeña 15 kg",
        "weight_kg": 15.0,
        "cost_price": 50900.0,
        "margin_percent": 20.0,
        "sale_price": 61080.0,
        "list_price": 70242.0,
        "stock_qty": 50,
        "sku": "AGIL-MINI-15",
        "is_default": 0
      },
      {
        "presentation_name": "Adulto 20 kg",
        "weight_kg": 20.0,
        "cost_price": 55400.0,
        "margin_percent": 20.0,
        "sale_price": 66480.0,
        "list_price": 76452.0,
        "stock_qty": 50,
        "sku": "AGIL-AD-20",
        "is_default": 1
      },
      {
        "presentation_name": "Cachorro 20 kg",
        "weight_kg": 20.0,
        "cost_price": 63700.0,
        "margin_percent": 20.0,
        "sale_price": 76440.0,
        "list_price": 87906.0,
        "stock_qty": 50,
        "sku": "AGIL-CACH-20",
        "is_default": 0
      }
    ]
  },
  {
    "id": 68,
    "category_id": 2,
    "brand_id": 25,
    "name": "Agility Cat (Adulto, Kitten, Urinary)",
    "slug": "agility-cat",
    "description": "Nutrición felina con salmón y pollo, enriquecido con taurina y pH controlado para evitar cálculos.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 10 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_615731-MLA100085791445_122025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Cat Adulto 10 kg",
        "weight_kg": 10.0,
        "cost_price": 55900.0,
        "margin_percent": 20.0,
        "sale_price": 67080.0,
        "list_price": 77142.0,
        "stock_qty": 50,
        "sku": "AGIL-CAT-AD-10",
        "is_default": 1
      },
      {
        "presentation_name": "Cat Kitten 10 kg",
        "weight_kg": 10.0,
        "cost_price": 60500.0,
        "margin_percent": 20.0,
        "sale_price": 72600.0,
        "list_price": 83490.0,
        "stock_qty": 50,
        "sku": "AGIL-CAT-KIT-10",
        "is_default": 0
      },
      {
        "presentation_name": "Cat Urinary 10 kg",
        "weight_kg": 10.0,
        "cost_price": 60500.0,
        "margin_percent": 20.0,
        "sale_price": 72600.0,
        "list_price": 83490.0,
        "stock_qty": 50,
        "sku": "AGIL-CAT-URIN-10",
        "is_default": 0
      }
    ]
  },
  {
    "id": 69,
    "category_id": 1,
    "brand_id": 26,
    "name": "Maxxium Adulto Cordero Patagónico y Arroz",
    "slug": "maxxium-adulto-cordero",
    "description": "Fórmula gourmet hipoalergénica con cordero patagónico natural para perros con paladar exigente.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Cordero Patagónico",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_615731-MLA100085791445_122025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 57200.0,
        "margin_percent": 20.0,
        "sale_price": 68640.0,
        "list_price": 78936.0,
        "stock_qty": 50,
        "sku": "MAXX-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 70,
    "category_id": 2,
    "brand_id": 27,
    "name": "7 Vidas Gato Adulto Carne y Pollo / Salmón",
    "slug": "7-vidas-gato-adulto",
    "description": "Alimento sabroso y económico para gatos con nutrientes indispensables para su vitalidad diaria.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 10 kg",
    "image_url": "https://http2.mlstatic.com/D_Q_NP_2X_851344-MLA110627789901_042026-T.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "10 kg",
        "weight_kg": 10.0,
        "cost_price": 40600.0,
        "margin_percent": 20.0,
        "sale_price": 48720.0,
        "list_price": 56028.0,
        "stock_qty": 50,
        "sku": "7VIDAS-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 71,
    "category_id": 1,
    "brand_id": 19,
    "name": "Tiernitos Perro Adulto Carne & Vegetales (22 kg)",
    "slug": "tiernitos-perro-adulto",
    "description": "Alimento clásico muy rendidor y apetecible con bocaditos tiernos sabor carne y cereales seleccionados.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 22 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_795475-MLA99878002573_112025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "22 kg",
        "weight_kg": 22.0,
        "cost_price": 32400.0,
        "margin_percent": 20.0,
        "sale_price": 38880.0,
        "list_price": 44712.0,
        "stock_qty": 50,
        "sku": "TIERN-22",
        "is_default": 1
      }
    ]
  },
  {
    "id": 72,
    "category_id": 1,
    "brand_id": 19,
    "name": "Tiernitos Cachorros (22 kg)",
    "slug": "tiernitos-cachorros",
    "description": "Excelente relación precio-calidad para camadas de cachorros activos en crecimiento.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Bolsa 22 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_704334-MLA99335499802_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "22 kg",
        "weight_kg": 22.0,
        "cost_price": 36700.0,
        "margin_percent": 20.0,
        "sale_price": 44040.0,
        "list_price": 50646.0,
        "stock_qty": 50,
        "sku": "TIERN-CACH-22",
        "is_default": 1
      }
    ]
  },
  {
    "id": 73,
    "category_id": 3,
    "brand_id": 19,
    "name": "Tiernitos Snacks Dentales & Masticables 3+1",
    "slug": "tiernitos-snacks-dentales",
    "description": "Barras masticables funcionales con clorofila y hexametafosfato para combatir el mal aliento.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "Snack Dental",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_876741-MLU79111404727_092024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Snack Estrella 120g",
        "weight_kg": 0.12,
        "cost_price": 1500.0,
        "margin_percent": 35.0,
        "sale_price": 2025.0,
        "list_price": 2329.0,
        "stock_qty": 50,
        "sku": "TIERN-ESTRELLA",
        "is_default": 0
      },
      {
        "presentation_name": "Raza Pequeña 3+1",
        "weight_kg": 0.15,
        "cost_price": 1150.0,
        "margin_percent": 35.0,
        "sale_price": 1552.0,
        "list_price": 1785.0,
        "stock_qty": 50,
        "sku": "TIERN-SNACK-PEQ",
        "is_default": 1
      },
      {
        "presentation_name": "Raza Mediana/Grande 3+1",
        "weight_kg": 0.25,
        "cost_price": 1350.0,
        "margin_percent": 35.0,
        "sale_price": 1823.0,
        "list_price": 2096.0,
        "stock_qty": 50,
        "sku": "TIERN-SNACK-MED",
        "is_default": 0
      }
    ]
  },
  {
    "id": 74,
    "category_id": 1,
    "brand_id": 20,
    "name": "Rosco Perro Carne y Pollo / Cocktail (22 kg)",
    "slug": "rosco-perro-carne-pollo",
    "description": "Alimento balanceado hiper accesible para familias y comederos comunitarios.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 22 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_817905-MLA99842229311_112025-O.webp",
    "is_featured": 0,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 18200.0,
        "margin_percent": 20.0,
        "sale_price": 21840.0,
        "list_price": 25116.0,
        "stock_qty": 50,
        "sku": "ROSCO-15",
        "is_default": 0
      },
      {
        "presentation_name": "22 kg Gigante",
        "weight_kg": 22.0,
        "cost_price": 25100.0,
        "margin_percent": 20.0,
        "sale_price": 30120.0,
        "list_price": 34638.0,
        "stock_qty": 50,
        "sku": "ROSCO-22",
        "is_default": 1
      }
    ]
  },
  {
    "id": 75,
    "category_id": 1,
    "brand_id": 21,
    "name": "Pacha Perro Adulto Cocktail / Mix",
    "slug": "pacha-perro-adulto",
    "description": "Bolsa económica clásica con cereales tostados y grasa animal seleccionada.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Económico",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_817905-MLA99842229311_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "10 kg",
        "weight_kg": 10.0,
        "cost_price": 12700.0,
        "margin_percent": 22.0,
        "sale_price": 15494.0,
        "list_price": 17818.0,
        "stock_qty": 50,
        "sku": "PACHA-10",
        "is_default": 0
      },
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 18600.0,
        "margin_percent": 20.0,
        "sale_price": 22320.0,
        "list_price": 25668.0,
        "stock_qty": 50,
        "sku": "PACHA-15",
        "is_default": 0
      },
      {
        "presentation_name": "20 kg",
        "weight_kg": 20.0,
        "cost_price": 24000.0,
        "margin_percent": 20.0,
        "sale_price": 28800.0,
        "list_price": 33120.0,
        "stock_qty": 50,
        "sku": "PACHA-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 76,
    "category_id": 1,
    "brand_id": 22,
    "name": "Chacal Perro Adulto (22 kg)",
    "slug": "chacal-perro-adulto",
    "description": "La bolsa más económica del mercado para perros grandes y de campo.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Hiper Económico",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_817905-MLA99842229311_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 16400.0,
        "margin_percent": 20.0,
        "sale_price": 19680.0,
        "list_price": 22632.0,
        "stock_qty": 50,
        "sku": "CHACAL-15",
        "is_default": 0
      },
      {
        "presentation_name": "22 kg",
        "weight_kg": 22.0,
        "cost_price": 23400.0,
        "margin_percent": 20.0,
        "sale_price": 28080.0,
        "list_price": 32292.0,
        "stock_qty": 50,
        "sku": "CHACAL-22",
        "is_default": 1
      }
    ]
  },
  {
    "id": 77,
    "category_id": 1,
    "brand_id": 24,
    "name": "Raza Nutripet Perro Carne y Pollo",
    "slug": "raza-nutripet-perro",
    "description": "Alimento completo con fibras naturales y cereales seleccionados para digestión equilibrada.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Bolsa 20 kg",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_817905-MLA99842229311_112025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "15 kg",
        "weight_kg": 15.0,
        "cost_price": 23100.0,
        "margin_percent": 20.0,
        "sale_price": 27720.0,
        "list_price": 31878.0,
        "stock_qty": 50,
        "sku": "RAZA-15",
        "is_default": 0
      },
      {
        "presentation_name": "20 kg",
        "weight_kg": 20.0,
        "cost_price": 29750.0,
        "margin_percent": 20.0,
        "sale_price": 35700.0,
        "list_price": 41055.0,
        "stock_qty": 50,
        "sku": "RAZA-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 78,
    "category_id": 3,
    "brand_id": 28,
    "name": "Huesos Prensados de Cuero Vacuno Blanco 100% Natural",
    "slug": "huesos-prensados-cuero-vacuno",
    "description": "Huesos masticables de cuero vacuno seleccionados. Calman la ansiedad, fortalecen encías y limpian sarro.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "100% Natural",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_876741-MLU79111404727_092024-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Hueso N°1 Chico (3-4 pulgadas)",
        "weight_kg": 0.05,
        "cost_price": 800.0,
        "margin_percent": 35.0,
        "sale_price": 1080.0,
        "list_price": 1242.0,
        "stock_qty": 50,
        "sku": "HUESO-1",
        "is_default": 0
      },
      {
        "presentation_name": "Hueso N°2 Mediano (7-8 pulgadas)",
        "weight_kg": 0.12,
        "cost_price": 1300.0,
        "margin_percent": 35.0,
        "sale_price": 1755.0,
        "list_price": 2018.0,
        "stock_qty": 50,
        "sku": "HUESO-2",
        "is_default": 0
      },
      {
        "presentation_name": "Hueso N°3 Grande (8-9 pulgadas)",
        "weight_kg": 0.22,
        "cost_price": 3100.0,
        "margin_percent": 35.0,
        "sale_price": 4185.0,
        "list_price": 4813.0,
        "stock_qty": 50,
        "sku": "HUESO-3",
        "is_default": 1
      },
      {
        "presentation_name": "Hueso N°4 Extra Grande (9-10 pulgadas)",
        "weight_kg": 0.35,
        "cost_price": 4440.0,
        "margin_percent": 35.0,
        "sale_price": 5994.0,
        "list_price": 6893.0,
        "stock_qty": 50,
        "sku": "HUESO-4",
        "is_default": 0
      },
      {
        "presentation_name": "Hueso N°5 Gigante (10-11 pulgadas)",
        "weight_kg": 0.5,
        "cost_price": 4700.0,
        "margin_percent": 35.0,
        "sale_price": 6345.0,
        "list_price": 7297.0,
        "stock_qty": 50,
        "sku": "HUESO-5",
        "is_default": 0
      }
    ]
  },
  {
    "id": 79,
    "category_id": 3,
    "brand_id": 28,
    "name": "Orejas de Vaca Especial Deshidratadas para Perro",
    "slug": "orejas-de-vaca-deshidratadas",
    "description": "Golosina recreativa 100% cartílago digestible natural. Ideal para mantener entretenido a tu perro horas enteras.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "Masticable Premium",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_876741-MLU79111404727_092024-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Unidad Especial",
        "weight_kg": 0.08,
        "cost_price": 800.0,
        "margin_percent": 35.0,
        "sale_price": 1080.0,
        "list_price": 1242.0,
        "stock_qty": 50,
        "sku": "OREJA-1",
        "is_default": 1
      }
    ]
  },
  {
    "id": 80,
    "category_id": 3,
    "brand_id": 28,
    "name": "Caramelos y Palitos Masticables Saborizados",
    "slug": "caramelos-palitos-masticables",
    "description": "Pack de palitos sabrosos de cuero y cereales para mimar a tu mascota todos los días.",
    "pet_type": "perros",
    "subcat": "snacks",
    "breed_size": "todas",
    "badge": "Pack Masticable",
    "image_url": "https://resources.claroshop.com/medios-plazavip/mkt/646d0036c12bf_6jpg.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Pack Grande",
        "weight_kg": 0.4,
        "cost_price": 6800.0,
        "margin_percent": 35.0,
        "sale_price": 9180.0,
        "list_price": 10557.0,
        "stock_qty": 50,
        "sku": "PALITOS-PACK",
        "is_default": 1
      }
    ]
  },
  {
    "id": 81,
    "category_id": 4,
    "brand_id": 29,
    "name": "Piedras Sanitarias Absorsol Clásicas",
    "slug": "piedras-sanitarias-absorsol",
    "description": "Piedras naturales absorbentes minerales que neutralizan olores y mantienen la bandeja seca y limpia.",
    "pet_type": "gatos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Bolsa Ahorro",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_767034-MLU73676996172_012024-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Bolsa 8 kg",
        "weight_kg": 8.0,
        "cost_price": 6100.0,
        "margin_percent": 30.0,
        "sale_price": 7930.0,
        "list_price": 9120.0,
        "stock_qty": 50,
        "sku": "ABSOR-8",
        "is_default": 0
      },
      {
        "presentation_name": "Bulto 12 kg (6x2kg)",
        "weight_kg": 12.0,
        "cost_price": 10100.0,
        "margin_percent": 25.0,
        "sale_price": 12625.0,
        "list_price": 14519.0,
        "stock_qty": 50,
        "sku": "ABSOR-12",
        "is_default": 1
      },
      {
        "presentation_name": "Bulto 21.6 kg (6x3.6kg)",
        "weight_kg": 21.6,
        "cost_price": 16850.0,
        "margin_percent": 20.0,
        "sale_price": 20220.0,
        "list_price": 23253.0,
        "stock_qty": 50,
        "sku": "ABSOR-21.6",
        "is_default": 0
      }
    ]
  },
  {
    "id": 82,
    "category_id": 4,
    "brand_id": 29,
    "name": "Piedras Sanitarias Alta Gama Perfumadas",
    "slug": "piedras-sanitarias-alta-gama-perfumada",
    "description": "Mineral ultra poroso con suave aroma a lavanda que se activa con la humedad. Cero polvo y máxima absorción.",
    "pet_type": "gatos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Aroma Lavanda",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_768895-MLA99563539018_122025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Bulto 12 kg (6x2kg)",
        "weight_kg": 12.0,
        "cost_price": 14700.0,
        "margin_percent": 25.0,
        "sale_price": 18375.0,
        "list_price": 21131.0,
        "stock_qty": 50,
        "sku": "ALTGAMA-12",
        "is_default": 1
      },
      {
        "presentation_name": "Bulto 21.6 kg (6x3.6kg)",
        "weight_kg": 21.6,
        "cost_price": 25500.0,
        "margin_percent": 20.0,
        "sale_price": 30600.0,
        "list_price": 35190.0,
        "stock_qty": 50,
        "sku": "ALTGAMA-21.6",
        "is_default": 0
      }
    ]
  },
  {
    "id": 83,
    "category_id": 4,
    "brand_id": 29,
    "name": "Piedras Sanitarias Pipicat Aglutinantes (Bentonita)",
    "slug": "pipicat-piedras-aglutinantes",
    "description": "Bentonita sódica aglutinante de máxima compresión. Forma terrones sólidos fáciles de retirar con pala sin desperdiciar.",
    "pet_type": "gatos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Aglutinante Pro",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_752804-MLA100008869329_122025-O.webp",
    "is_featured": 1,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bulto 24 kg (6x4kg)",
        "weight_kg": 24.0,
        "cost_price": 17800.0,
        "margin_percent": 20.0,
        "sale_price": 21360.0,
        "list_price": 24564.0,
        "stock_qty": 50,
        "sku": "PIPICAT-24",
        "is_default": 1
      }
    ]
  },
  {
    "id": 84,
    "category_id": 4,
    "brand_id": 29,
    "name": "Piedras Sanitarias Michi Feliz",
    "slug": "piedras-michi-feliz",
    "description": "Económicas y rendidoras. Mineral seleccionado para el uso cotidiano en hogares con múltiples gatos.",
    "pet_type": "gatos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Económicas",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_767034-MLU73676996172_012024-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bulto 10.8 kg (6x1.8kg)",
        "weight_kg": 10.8,
        "cost_price": 6450.0,
        "margin_percent": 30.0,
        "sale_price": 8385.0,
        "list_price": 9643.0,
        "stock_qty": 50,
        "sku": "MICHI-10.8",
        "is_default": 1
      }
    ]
  },
  {
    "id": 85,
    "category_id": 4,
    "brand_id": 29,
    "name": "Tronquitos Bediwood Colchón Sanitario Ecológico",
    "slug": "tronquitos-bediwood-colchon-sanitario",
    "description": "Pellets 100% de madera de pino virgen biodegradable. Absorben 3 veces su peso y desprenden aroma a pino natural.",
    "pet_type": "ambos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "100% Ecológico",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_752804-MLA100008869329_122025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 9500.0,
        "margin_percent": 25.0,
        "sale_price": 11875.0,
        "list_price": 13656.0,
        "stock_qty": 50,
        "sku": "BEDI-15",
        "is_default": 1
      },
      {
        "presentation_name": "Bulto 25 kg (5x5kg)",
        "weight_kg": 25.0,
        "cost_price": 14000.0,
        "margin_percent": 20.0,
        "sale_price": 16800.0,
        "list_price": 19320.0,
        "stock_qty": 50,
        "sku": "BEDI-25",
        "is_default": 0
      }
    ]
  },
  {
    "id": 86,
    "category_id": 5,
    "brand_id": 30,
    "name": "Shampoo Osspret Tradicional Pulguicida y Garrapaticida",
    "slug": "shampoo-osspret-tradicional",
    "description": "Tratamiento insecticida de uso profesional para perros y gatos. Elimina pulgas, garrapatas y piojos en el baño.",
    "pet_type": "ambos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Veterinaria",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_706344-MLA111706358457_052026-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Botella 250 ml",
        "weight_kg": 0.3,
        "cost_price": 6800.0,
        "margin_percent": 35.0,
        "sale_price": 9180.0,
        "list_price": 10557.0,
        "stock_qty": 50,
        "sku": "OSSP-TRAD-250",
        "is_default": 1
      }
    ]
  },
  {
    "id": 87,
    "category_id": 5,
    "brand_id": 30,
    "name": "Shampoo Osspret Double Belleza & Acondicionador",
    "slug": "shampoo-osspret-double",
    "description": "Fórmula 2 en 1 con agentes desenredantes y siliconas protectoras que aportan brillo y suavidad al pelaje.",
    "pet_type": "ambos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Belleza Canina",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_777998-MLA100083527255_122025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Botella 250 ml",
        "weight_kg": 0.3,
        "cost_price": 7400.0,
        "margin_percent": 35.0,
        "sale_price": 9990.0,
        "list_price": 11488.0,
        "stock_qty": 50,
        "sku": "OSSP-DOUB-250",
        "is_default": 1
      }
    ]
  },
  {
    "id": 88,
    "category_id": 5,
    "brand_id": 30,
    "name": "Shampoo Osspret Aqua Ecto PG (Ectoparasiticida)",
    "slug": "shampoo-osspret-aqua-ecto",
    "description": "Poderosa acción repelente y desparasitante con acción residual para proteger a mascotas expuestas al aire libre.",
    "pet_type": "perros",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Antiparasitario",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_764078-MLA99587766146_122025-O.webp",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Botella 250 ml",
        "weight_kg": 0.3,
        "cost_price": 6900.0,
        "margin_percent": 35.0,
        "sale_price": 9315.0,
        "list_price": 10712.0,
        "stock_qty": 50,
        "sku": "OSSP-ECTO-250",
        "is_default": 1
      }
    ]
  },
  {
    "id": 89,
    "category_id": 5,
    "brand_id": 30,
    "name": "Ecthol 5 Solución Pulguicida y Garrapaticida Concentrada",
    "slug": "ecthol-5-solucion-concentrada",
    "description": "Concentrado emulsionable para el control integral de ectoparásitos en perros e instalaciones del hogar.",
    "pet_type": "perros",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Línea Veterinaria",
    "image_url": "https://http2.mlstatic.com/D_NQ_NP_679728-MLA84083537587_042025-O.webp",
    "is_featured": 1,
    "is_promo": 1,
    "promo_tag": "OFERTA DESTACADA",
    "variants": [
      {
        "presentation_name": "Frasco 70 cc",
        "weight_kg": 0.1,
        "cost_price": 4700.0,
        "margin_percent": 35.0,
        "sale_price": 6345.0,
        "list_price": 7297.0,
        "stock_qty": 50,
        "sku": "ECTHOL-70",
        "is_default": 0
      },
      {
        "presentation_name": "Frasco 120 cc",
        "weight_kg": 0.15,
        "cost_price": 6600.0,
        "margin_percent": 35.0,
        "sale_price": 8910.0,
        "list_price": 10246.0,
        "stock_qty": 50,
        "sku": "ECTHOL-120",
        "is_default": 1
      }
    ]
  },
  {
    "id": 90,
    "category_id": 7,
    "brand_id": 31,
    "name": "Shulet Alimento Completo para Peces en Escamas / Hojuelas",
    "slug": "shulet-alimento-peces-escamas",
    "description": "Nutrición balanceada en hojuelas para peces de agua dulce y fría. Alta flotabilidad, no enturbia el agua y resalta la coloración natural de los peces.",
    "pet_type": "peces",
    "subcat": "alimento",
    "breed_size": "todas",
    "badge": "Acuarismo",
    "image_url": "https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "10 grs Nro. 1",
        "weight_kg": 0.01,
        "cost_price": 2100.0,
        "margin_percent": 30.0,
        "sale_price": 2730.0,
        "list_price": 2730.0,
        "stock_qty": 50,
        "sku": "SHU-PEC-10",
        "is_default": 0
      },
      {
        "presentation_name": "20 grs Nro. 2",
        "weight_kg": 0.02,
        "cost_price": 3600.0,
        "margin_percent": 30.0,
        "sale_price": 4680.0,
        "list_price": 4680.0,
        "stock_qty": 50,
        "sku": "SHU-PEC-20",
        "is_default": 0
      },
      {
        "presentation_name": "40 grs Nro. 3",
        "weight_kg": 0.04,
        "cost_price": 6700.0,
        "margin_percent": 25.0,
        "sale_price": 8375.0,
        "list_price": 8375.0,
        "stock_qty": 50,
        "sku": "SHU-PEC-40",
        "is_default": 1
      },
      {
        "presentation_name": "Caja Criador x 2.2 kg",
        "weight_kg": 2.2,
        "cost_price": 124400.0,
        "margin_percent": 20.0,
        "sale_price": 149280.0,
        "list_price": 149280.0,
        "stock_qty": 50,
        "sku": "SHU-PEC-2200",
        "is_default": 0
      }
    ]
  },
  {
    "id": 91,
    "category_id": 9,
    "brand_id": 32,
    "name": "Hor-Tal Hormiguicida Líquido Concentrado",
    "slug": "hortal-hormiguicida-liquido",
    "description": "Insecticida hormiguicida líquido de alta eficacia para el control de hormigas cortadoras y de jardín. Actúa por contacto e ingestión.",
    "pet_type": "sanidad",
    "subcat": "plagas",
    "breed_size": "todas",
    "badge": "Control de Plagas",
    "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Frasco 60 cc",
        "weight_kg": 0.06,
        "cost_price": 2750.0,
        "margin_percent": 30.0,
        "sale_price": 3575.0,
        "list_price": 3575.0,
        "stock_qty": 50,
        "sku": "HT-LIQ-60",
        "is_default": 0
      },
      {
        "presentation_name": "Frasco 120 cc",
        "weight_kg": 0.12,
        "cost_price": 3950.0,
        "margin_percent": 30.0,
        "sale_price": 5135.0,
        "list_price": 5135.0,
        "stock_qty": 50,
        "sku": "HT-LIQ-120",
        "is_default": 1
      },
      {
        "presentation_name": "Frasco 250 cc",
        "weight_kg": 0.25,
        "cost_price": 6500.0,
        "margin_percent": 25.0,
        "sale_price": 8125.0,
        "list_price": 8125.0,
        "stock_qty": 50,
        "sku": "HT-LIQ-250",
        "is_default": 0
      }
    ]
  },
  {
    "id": 92,
    "category_id": 9,
    "brand_id": 32,
    "name": "Hor-Tal Hormiguicida en Polvo Seco x 250 grs",
    "slug": "hortal-hormiguicida-polvo-250g",
    "description": "Hormiguicida en polvo seco listo para usar con talquera dosificadora. Ideal para aplicar directamente en caminos, bocas de hormigueros y zócalos.",
    "pet_type": "sanidad",
    "subcat": "plagas",
    "breed_size": "todas",
    "badge": "Uso Directo",
    "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Talquera 250 grs",
        "weight_kg": 0.25,
        "cost_price": 3550.0,
        "margin_percent": 30.0,
        "sale_price": 4615.0,
        "list_price": 4615.0,
        "stock_qty": 50,
        "sku": "HT-POLV-250",
        "is_default": 1
      }
    ]
  },
  {
    "id": 93,
    "category_id": 9,
    "brand_id": 32,
    "name": "Hor-Tal Mirex Hormiguicida Cebo Granulado x 250 grs",
    "slug": "hortal-mirex-cebo-granulado-250g",
    "description": "Cebo granulado de máxima atracción. Las hormigas transportan el gránulo al interior del hormiguero eliminando el hongo y la colonia entera.",
    "pet_type": "sanidad",
    "subcat": "plagas",
    "breed_size": "todas",
    "badge": "Cebo Granulado",
    "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Pote 250 grs",
        "weight_kg": 0.25,
        "cost_price": 2900.0,
        "margin_percent": 30.0,
        "sale_price": 3770.0,
        "list_price": 3770.0,
        "stock_qty": 50,
        "sku": "HT-MIR-250",
        "is_default": 1
      }
    ]
  },
  {
    "id": 94,
    "category_id": 9,
    "brand_id": 33,
    "name": "Fluido Manchester Desinfectante Concentrado Fenólico",
    "slug": "fluido-manchester-desinfectante",
    "description": "Desinfectante y germicida fenólico tradicional concentrado. Potente acción limpiadora y bactericida para caniles, patios, veredas y exteriores.",
    "pet_type": "sanidad",
    "subcat": "desinfeccion",
    "breed_size": "todas",
    "badge": "Desinfección Total",
    "image_url": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Envase 350 cc",
        "weight_kg": 0.35,
        "cost_price": 5300.0,
        "margin_percent": 28.0,
        "sale_price": 6784.0,
        "list_price": 6784.0,
        "stock_qty": 50,
        "sku": "FL-MAN-350",
        "is_default": 0
      },
      {
        "presentation_name": "Envase 700 cc",
        "weight_kg": 0.7,
        "cost_price": 11400.0,
        "margin_percent": 25.0,
        "sale_price": 14250.0,
        "list_price": 14250.0,
        "stock_qty": 50,
        "sku": "FL-MAN-700",
        "is_default": 1
      }
    ]
  },
  {
    "id": 95,
    "category_id": 9,
    "brand_id": 33,
    "name": "Fluido Triunfo Desinfectante Concentrado",
    "slug": "fluido-triunfo-desinfectante",
    "description": "Poderoso desinfectante y desodorizante para limpieza profunda de galpones, corrales, caniles y superficies del hogar.",
    "pet_type": "sanidad",
    "subcat": "desinfeccion",
    "breed_size": "todas",
    "badge": "Higiene Ambiental",
    "image_url": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Botella 500 cc",
        "weight_kg": 0.5,
        "cost_price": 3900.0,
        "margin_percent": 30.0,
        "sale_price": 5070.0,
        "list_price": 5070.0,
        "stock_qty": 50,
        "sku": "FL-TRI-500",
        "is_default": 0
      },
      {
        "presentation_name": "Botella 1000 cc (1 Litro)",
        "weight_kg": 1.0,
        "cost_price": 7100.0,
        "margin_percent": 25.0,
        "sale_price": 8875.0,
        "list_price": 8875.0,
        "stock_qty": 50,
        "sku": "FL-TRI-1000",
        "is_default": 1
      }
    ]
  },
  {
    "id": 96,
    "category_id": 9,
    "brand_id": 34,
    "name": "Geltex Cucarachicida Cebo en Estaciones x 6 unidades",
    "slug": "geltex-cucarachicida-cebo-6u",
    "description": "Estaciones de cebo listas para usar. Atracción continua y efecto retardado que elimina el nido sin olor ni vapores tóxicos.",
    "pet_type": "sanidad",
    "subcat": "plagas",
    "breed_size": "todas",
    "badge": "Efecto Dominó",
    "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Caja x 6 Cebos",
        "weight_kg": 0.1,
        "cost_price": 3100.0,
        "margin_percent": 30.0,
        "sale_price": 4030.0,
        "list_price": 4030.0,
        "stock_qty": 50,
        "sku": "GT-CEB-6",
        "is_default": 1
      }
    ]
  },
  {
    "id": 97,
    "category_id": 9,
    "brand_id": 34,
    "name": "Geltex Cucarachicida Gel en Jeringa Aplicadora",
    "slug": "geltex-cucarachicida-gel-jeringa",
    "description": "Gel insecticida de máxima eficacia para grietas, bajo mesadas y rincones difíciles. Muy alta palatabilidad para cucarachas alemanas y comunes.",
    "pet_type": "sanidad",
    "subcat": "plagas",
    "breed_size": "todas",
    "badge": "Acción Prolongada",
    "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Jeringa 6 grs",
        "weight_kg": 0.006,
        "cost_price": 3900.0,
        "margin_percent": 30.0,
        "sale_price": 5070.0,
        "list_price": 5070.0,
        "stock_qty": 50,
        "sku": "GT-JER-6",
        "is_default": 0
      },
      {
        "presentation_name": "Jeringa 12 grs",
        "weight_kg": 0.012,
        "cost_price": 5950.0,
        "margin_percent": 25.0,
        "sale_price": 7438.0,
        "list_price": 7438.0,
        "stock_qty": 50,
        "sku": "GT-JER-12",
        "is_default": 1
      }
    ]
  },
  {
    "id": 98,
    "category_id": 9,
    "brand_id": 34,
    "name": "Geltex Raticida Cebo Bloques Parafinados x 100 grs",
    "slug": "geltex-raticida-cebo-100g",
    "description": "Bloques rodenticidas resistentes a la humedad y lluvia. Diseñados para exteriores, galpones y desvanes.",
    "pet_type": "sanidad",
    "subcat": "plagas",
    "breed_size": "todas",
    "badge": "Cebo Parafinado",
    "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Estuche 100 grs",
        "weight_kg": 0.1,
        "cost_price": 4400.0,
        "margin_percent": 30.0,
        "sale_price": 5720.0,
        "list_price": 5720.0,
        "stock_qty": 50,
        "sku": "GT-RAT-100",
        "is_default": 1
      }
    ]
  },
  {
    "id": 99,
    "category_id": 9,
    "brand_id": 35,
    "name": "Ultra Raticida Rodenticida Cebo Monodósico en Sobres",
    "slug": "ultra-raticida-cebo-sobres",
    "description": "Rodenticida anticoagulante monodósico de última generación. Mata con una sola ingesta sin despertar recelo entre la colonia de roedores.",
    "pet_type": "sanidad",
    "subcat": "plagas",
    "breed_size": "todas",
    "badge": "Monodósico",
    "image_url": "https://images.unsplash.com/photo-1587593810167-a84920ea0781?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Sobre 50 grs",
        "weight_kg": 0.05,
        "cost_price": 2200.0,
        "margin_percent": 35.0,
        "sale_price": 2970.0,
        "list_price": 2970.0,
        "stock_qty": 50,
        "sku": "ULT-SOB-50",
        "is_default": 0
      },
      {
        "presentation_name": "Dispenser 30 Sobres x 50 grs",
        "weight_kg": 1.5,
        "cost_price": 58500.0,
        "margin_percent": 20.0,
        "sale_price": 70200.0,
        "list_price": 70200.0,
        "stock_qty": 50,
        "sku": "ULT-DISP-30",
        "is_default": 1
      }
    ]
  },
  {
    "id": 100,
    "category_id": 8,
    "brand_id": 36,
    "name": "Prenut Parrillero Doméstico Bebé (Iniciador)",
    "slug": "prenut-parrillero-bebe-25kg",
    "description": "Alimento balanceado completo formulado para pollitos parrilleros en su fase inicial de vida. Alto contenido proteico y vitamínico.",
    "pet_type": "granja",
    "subcat": "aves",
    "breed_size": "todas",
    "badge": "Línea Granja",
    "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 25 kg",
        "weight_kg": 25.0,
        "cost_price": 17600.0,
        "margin_percent": 20.0,
        "sale_price": 21120.0,
        "list_price": 21120.0,
        "stock_qty": 50,
        "sku": "PREN-PARR-BEB-25",
        "is_default": 1
      }
    ]
  },
  {
    "id": 101,
    "category_id": 8,
    "brand_id": 36,
    "name": "Prenut Parrillero Doméstico Engorde (Terminador)",
    "slug": "prenut-parrillero-engorde-25kg",
    "description": "Fórmula balanceada para pollos en etapa de engorde y terminación. Rápido desarrollo muscular y excelente conversión alimenticia.",
    "pet_type": "granja",
    "subcat": "aves",
    "breed_size": "todas",
    "badge": "Línea Granja",
    "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 25 kg",
        "weight_kg": 25.0,
        "cost_price": 17400.0,
        "margin_percent": 20.0,
        "sale_price": 20880.0,
        "list_price": 20880.0,
        "stock_qty": 50,
        "sku": "PREN-PARR-ENG-25",
        "is_default": 1
      }
    ]
  },
  {
    "id": 102,
    "category_id": 8,
    "brand_id": 36,
    "name": "Prenut Ponedora Doméstica Postura (Gallinas)",
    "slug": "prenut-ponedora-postura-25kg",
    "description": "Alimento para gallinas ponedoras con niveles balanceados de calcio y fósforo para una cáscara fuerte y máxima postura diaria.",
    "pet_type": "granja",
    "subcat": "aves",
    "breed_size": "todas",
    "badge": "Alta Postura",
    "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 25 kg",
        "weight_kg": 25.0,
        "cost_price": 17200.0,
        "margin_percent": 20.0,
        "sale_price": 20640.0,
        "list_price": 20640.0,
        "stock_qty": 50,
        "sku": "PREN-PONE-25",
        "is_default": 1
      }
    ]
  },
  {
    "id": 103,
    "category_id": 8,
    "brand_id": 36,
    "name": "Prenut Conejo Doméstico Alimento Balanceado",
    "slug": "prenut-conejo-domestico-25kg",
    "description": "Nutrición en pellets formulada con alfalfa y fibras de alta digestibilidad. Favorece el desgaste dental natural y la salud gastrointestinal.",
    "pet_type": "roedores",
    "subcat": "roedores",
    "breed_size": "todas",
    "badge": "Roedores y Granja",
    "image_url": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 25 kg",
        "weight_kg": 25.0,
        "cost_price": 17600.0,
        "margin_percent": 20.0,
        "sale_price": 21120.0,
        "list_price": 21120.0,
        "stock_qty": 50,
        "sku": "PREN-CON-25",
        "is_default": 1
      }
    ]
  },
  {
    "id": 104,
    "category_id": 8,
    "brand_id": 36,
    "name": "Prenut Pájaro Pellets Extrusados x 3 mm",
    "slug": "prenut-pajaro-pellets-3mm-25kg",
    "description": "Pellets homogéneos extruidos de 3 mm para pájaros y aves de jaula. Aporte balanceado que evita la selección selectiva de semillas.",
    "pet_type": "aves_granja",
    "subcat": "aves",
    "breed_size": "todas",
    "badge": "Aves de Jaula",
    "image_url": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 25 kg",
        "weight_kg": 25.0,
        "cost_price": 33000.0,
        "margin_percent": 20.0,
        "sale_price": 39600.0,
        "list_price": 39600.0,
        "stock_qty": 50,
        "sku": "PREN-PAJ-25",
        "is_default": 1
      }
    ]
  },
  {
    "id": 105,
    "category_id": 8,
    "brand_id": 37,
    "name": "Maíz Entero y Maíz Partido de Selección",
    "slug": "maiz-entero-partido-seleccion",
    "description": "Granos de maíz secos y limpios de primera calidad. Excelente fuente calórica y de almidón para aves de corral y animales de granja.",
    "pet_type": "granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "Grano Limpio",
    "image_url": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Maíz Partido Grueso 24 kg",
        "weight_kg": 24.0,
        "cost_price": 9900.0,
        "margin_percent": 22.0,
        "sale_price": 12078.0,
        "list_price": 12078.0,
        "stock_qty": 50,
        "sku": "SEM-MAIZ-PART-24",
        "is_default": 0
      },
      {
        "presentation_name": "Maíz Entero 38 kg",
        "weight_kg": 38.0,
        "cost_price": 14990.0,
        "margin_percent": 20.0,
        "sale_price": 17988.0,
        "list_price": 17988.0,
        "stock_qty": 50,
        "sku": "SEM-MAIZ-ENT-38",
        "is_default": 1
      }
    ]
  },
  {
    "id": 106,
    "category_id": 8,
    "brand_id": 37,
    "name": "Mezcla Forrajera Especial para Gallinas",
    "slug": "mezcla-forrajera-gallina",
    "description": "Combinación balanceada de granos enteros y partidos (trigo, maíz, sorgo, avena) para aves de corral y gallinas camperas.",
    "pet_type": "granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "Forrajera",
    "image_url": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Mezcla Gallina STM 24 kg",
        "weight_kg": 24.0,
        "cost_price": 11900.0,
        "margin_percent": 22.0,
        "sale_price": 14518.0,
        "list_price": 14518.0,
        "stock_qty": 50,
        "sku": "SEM-GAL-STM-24",
        "is_default": 0
      },
      {
        "presentation_name": "Mezcla Gallina Especial 24 kg",
        "weight_kg": 24.0,
        "cost_price": 12000.0,
        "margin_percent": 22.0,
        "sale_price": 14640.0,
        "list_price": 14640.0,
        "stock_qty": 50,
        "sku": "SEM-GAL-ESP-24",
        "is_default": 1
      },
      {
        "presentation_name": "Mezcla Gallina Lumpy 24 kg",
        "weight_kg": 24.0,
        "cost_price": 14500.0,
        "margin_percent": 22.0,
        "sale_price": 17690.0,
        "list_price": 17690.0,
        "stock_qty": 50,
        "sku": "SEM-GAL-LUMP-24",
        "is_default": 0
      }
    ]
  },
  {
    "id": 107,
    "category_id": 8,
    "brand_id": 37,
    "name": "Avena Entera y Arrollada Forrajera",
    "slug": "avena-forrajera-30kg",
    "description": "Avena pura de campo de alta palatabilidad. Excelente aporte de fibra digestible y energía para caballos, conejos y aves.",
    "pet_type": "granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "100% Pura",
    "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 30 kg",
        "weight_kg": 30.0,
        "cost_price": 12500.0,
        "margin_percent": 20.0,
        "sale_price": 15000.0,
        "list_price": 15000.0,
        "stock_qty": 50,
        "sku": "SEM-AVEN-30",
        "is_default": 1
      }
    ]
  },
  {
    "id": 108,
    "category_id": 8,
    "brand_id": 37,
    "name": "Semillas de Girasol Confitero Seleccionado",
    "slug": "girasol-confitero-aves",
    "description": "Semillas de girasol confitero grande y carnoso con cáscara delgada. Ricas en ácidos grasos esenciales y vitaminas.",
    "pet_type": "aves_granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "Calidad Superior",
    "image_url": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 7500.0,
        "margin_percent": 25.0,
        "sale_price": 9375.0,
        "list_price": 9375.0,
        "stock_qty": 50,
        "sku": "SEM-GIR-10",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 20 kg",
        "weight_kg": 20.0,
        "cost_price": 12800.0,
        "margin_percent": 22.0,
        "sale_price": 15616.0,
        "list_price": 15616.0,
        "stock_qty": 50,
        "sku": "SEM-GIR-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 109,
    "category_id": 8,
    "brand_id": 37,
    "name": "Alpiste Clasificado Puro Doble Zaranda",
    "slug": "alpiste-clasificado-puro",
    "description": "Alpiste seleccionado de doble zaranda, libre de polvo y residuos. Alimento básico para canarios, jilgueros y aves canoras.",
    "pet_type": "aves_granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "Doble Zaranda",
    "image_url": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 18000.0,
        "margin_percent": 25.0,
        "sale_price": 22500.0,
        "list_price": 22500.0,
        "stock_qty": 50,
        "sku": "SEM-ALP-10",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 30 kg",
        "weight_kg": 30.0,
        "cost_price": 40000.0,
        "margin_percent": 20.0,
        "sale_price": 48000.0,
        "list_price": 48000.0,
        "stock_qty": 50,
        "sku": "SEM-ALP-30",
        "is_default": 1
      }
    ]
  },
  {
    "id": 110,
    "category_id": 8,
    "brand_id": 37,
    "name": "Mijo Clasificado Amarillo / Blanco",
    "slug": "mijo-clasificado-grano",
    "description": "Grano de mijo clasificado y calibrado. Fácil de descascarar, altamente digestible para periquitos, cotorras y aves silvestres.",
    "pet_type": "aves_granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "Grano Selecto",
    "image_url": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 9500.0,
        "margin_percent": 25.0,
        "sale_price": 11875.0,
        "list_price": 11875.0,
        "stock_qty": 50,
        "sku": "SEM-MIJ-10",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 30 kg",
        "weight_kg": 30.0,
        "cost_price": 24000.0,
        "margin_percent": 20.0,
        "sale_price": 28800.0,
        "list_price": 28800.0,
        "stock_qty": 50,
        "sku": "SEM-MIJ-30",
        "is_default": 1
      }
    ]
  },
  {
    "id": 111,
    "category_id": 8,
    "brand_id": 37,
    "name": "Mezcla Nutricional para Canarios de Canto",
    "slug": "mezcla-canario-canto",
    "description": "Fórmula tradicional para canarios con alpiste, colza, nabo, lino y mijo. Favorece el brillo del plumaje y la vitalidad del canto.",
    "pet_type": "aves_granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "Canto y Vitalidad",
    "image_url": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 17900.0,
        "margin_percent": 25.0,
        "sale_price": 22375.0,
        "list_price": 22375.0,
        "stock_qty": 50,
        "sku": "SEM-CAN-10",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 30 kg",
        "weight_kg": 30.0,
        "cost_price": 49500.0,
        "margin_percent": 20.0,
        "sale_price": 59400.0,
        "list_price": 59400.0,
        "stock_qty": 50,
        "sku": "SEM-CAN-30",
        "is_default": 1
      }
    ]
  },
  {
    "id": 112,
    "category_id": 8,
    "brand_id": 37,
    "name": "Mezcla para Cardenales y Pájaros Silvestres",
    "slug": "mezcla-cardenal-silvestres",
    "description": "Mezcla rica en girasol chico, alpiste, avena pelada y granos seleccionados para cardenales, corbatitas y aves autóctonas.",
    "pet_type": "aves_granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "Silvestres",
    "image_url": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 9500.0,
        "margin_percent": 25.0,
        "sale_price": 11875.0,
        "list_price": 11875.0,
        "stock_qty": 50,
        "sku": "SEM-CARD-10",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 30 kg",
        "weight_kg": 30.0,
        "cost_price": 26500.0,
        "margin_percent": 20.0,
        "sale_price": 31800.0,
        "list_price": 31800.0,
        "stock_qty": 50,
        "sku": "SEM-CARD-30",
        "is_default": 1
      }
    ]
  },
  {
    "id": 113,
    "category_id": 8,
    "brand_id": 37,
    "name": "Polenta Pura de Maíz Forrajera y Familiar",
    "slug": "polenta-maiz-forrajera-25kg",
    "description": "Sémola pura de maíz amarillo sin aditivos. Fácil de hidratar y cocinar para preparación de papillas y suplementos animales.",
    "pet_type": "granja",
    "subcat": "semillas",
    "breed_size": "todas",
    "badge": "100% Maíz",
    "image_url": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 25 kg",
        "weight_kg": 25.0,
        "cost_price": 18300.0,
        "margin_percent": 20.0,
        "sale_price": 21960.0,
        "list_price": 21960.0,
        "stock_qty": 50,
        "sku": "SEM-POL-25",
        "is_default": 1
      }
    ]
  },
  {
    "id": 114,
    "category_id": 1,
    "brand_id": 18,
    "name": "Arroz Saborizado Gran Campeón para Perros",
    "slug": "arroz-saborizado-gran-campeon",
    "description": "Arroz especialmente acondicionado y enriquecido para mezclar con carne o alimento balanceado. Cocción rápida y alta asimilación digestiva.",
    "pet_type": "perros",
    "subcat": "complementos",
    "breed_size": "todas",
    "badge": "Cocción Rápida",
    "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Tradicional 15 kg",
        "weight_kg": 15.0,
        "cost_price": 12500.0,
        "margin_percent": 25.0,
        "sale_price": 15625.0,
        "list_price": 15625.0,
        "stock_qty": 50,
        "sku": "GC-ARR-TRAD-15",
        "is_default": 0
      },
      {
        "presentation_name": "Premium 15 kg",
        "weight_kg": 15.0,
        "cost_price": 13400.0,
        "margin_percent": 25.0,
        "sale_price": 16750.0,
        "list_price": 16750.0,
        "stock_qty": 50,
        "sku": "GC-ARR-PREM-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 115,
    "category_id": 1,
    "brand_id": 18,
    "name": "Arroz Partido de Segunda Económico para Perros",
    "slug": "arroz-partido-economico-30kg",
    "description": "Arroz partido económico para hervir y complementar dietas caninas caseras o en refugios. Gran rendimiento.",
    "pet_type": "perros",
    "subcat": "complementos",
    "breed_size": "todas",
    "badge": "Súper Económico",
    "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 30 kg",
        "weight_kg": 30.0,
        "cost_price": 23500.0,
        "margin_percent": 20.0,
        "sale_price": 28200.0,
        "list_price": 28200.0,
        "stock_qty": 50,
        "sku": "GC-ARR-PART-30",
        "is_default": 1
      }
    ]
  },
  {
    "id": 116,
    "category_id": 1,
    "brand_id": 18,
    "name": "Fideos Cocktail Gran Campeón para Perro",
    "slug": "fideos-cocktail-gran-campeon-10kg",
    "description": "Fideos secos especiales para mezclar con caldo, carne o alimento seco. Fuente práctica y económica de carbohidratos.",
    "pet_type": "perros",
    "subcat": "complementos",
    "breed_size": "todas",
    "badge": "Guarnición Canina",
    "image_url": "https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 7500.0,
        "margin_percent": 25.0,
        "sale_price": 9375.0,
        "list_price": 9375.0,
        "stock_qty": 50,
        "sku": "GC-FID-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 117,
    "category_id": 1,
    "brand_id": 17,
    "name": "Protemix Perro Adulto Carne y Cereales",
    "slug": "protemix-adulto-carne-cereales",
    "description": "Alimento completo y balanceado con proteína animal y cereales seleccionados. Garantiza deposiciones firmes y pelaje brillante.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "mediana",
    "badge": "Calidad Saladillo",
    "image_url": "https://images.unsplash.com/photo-1568640347023-a616a30bc3bd?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 29100.0,
        "margin_percent": 25.0,
        "sale_price": 36375.0,
        "list_price": 36375.0,
        "stock_qty": 50,
        "sku": "PROT-AD-15",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 21 kg",
        "weight_kg": 21.0,
        "cost_price": 38300.0,
        "margin_percent": 22.0,
        "sale_price": 46726.0,
        "list_price": 46726.0,
        "stock_qty": 50,
        "sku": "PROT-AD-21",
        "is_default": 1
      }
    ]
  },
  {
    "id": 118,
    "category_id": 1,
    "brand_id": 17,
    "name": "Protemix Perro Adulto Raza Pequeña",
    "slug": "protemix-adulto-raza-pequena",
    "description": "Croquetas diseñadas para la mandíbula de perros pequeños. Mayor concentración energética y sabor irresistible.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "pequeña",
    "badge": "Mordida Chica",
    "image_url": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 29100.0,
        "margin_percent": 25.0,
        "sale_price": 36375.0,
        "list_price": 36375.0,
        "stock_qty": 50,
        "sku": "PROT-MINI-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 119,
    "category_id": 1,
    "brand_id": 17,
    "name": "Protemix Perro Cachorro Crecimiento",
    "slug": "protemix-cachorro-crecimiento",
    "description": "Fórmula para cachorros con calcio y fósforo equilibrados para un crecimiento óseo armónico y fuerte.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros",
    "image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 22600.0,
        "margin_percent": 25.0,
        "sale_price": 28250.0,
        "list_price": 28250.0,
        "stock_qty": 50,
        "sku": "PROT-CACH-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 120,
    "category_id": 2,
    "brand_id": 17,
    "name": "Protemix Gato Adulto Pescado y Pollo",
    "slug": "protemix-gato-adulto",
    "description": "Nutrición felina con taurina y pH urinario controlado. Proteínas nobles de pescado y pollo para una óptima vitalidad.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Gatos Adultos",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 33100.0,
        "margin_percent": 25.0,
        "sale_price": 41375.0,
        "list_price": 41375.0,
        "stock_qty": 50,
        "sku": "PROT-GAT-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 121,
    "category_id": 1,
    "brand_id": 18,
    "name": "Gran Campeón Perro Adulto (Carne / Tradicional / Mantenimiento)",
    "slug": "gran-campeon-perro-adulto",
    "description": "Línea económica líder por su excelente relación costo-beneficio. Aporte calórico ideal para perros familiares y de guardia.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Económico",
    "image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Perro Carne 21 kg",
        "weight_kg": 21.0,
        "cost_price": 27650.0,
        "margin_percent": 22.0,
        "sale_price": 33733.0,
        "list_price": 33733.0,
        "stock_qty": 50,
        "sku": "GC-CARN-21",
        "is_default": 1
      },
      {
        "presentation_name": "Perro Tradicional 21 kg",
        "weight_kg": 21.0,
        "cost_price": 27650.0,
        "margin_percent": 22.0,
        "sale_price": 33733.0,
        "list_price": 33733.0,
        "stock_qty": 50,
        "sku": "GC-TRAD-21",
        "is_default": 0
      },
      {
        "presentation_name": "Mantenimiento 21 kg",
        "weight_kg": 21.0,
        "cost_price": 24700.0,
        "margin_percent": 22.0,
        "sale_price": 30134.0,
        "list_price": 30134.0,
        "stock_qty": 50,
        "sku": "GC-MANT-21",
        "is_default": 0
      }
    ]
  },
  {
    "id": 122,
    "category_id": 1,
    "brand_id": 18,
    "name": "Gran Campeón Cachorros",
    "slug": "gran-campeon-cachorros-10kg",
    "description": "Alimento completo para cachorros en desarrollo. Enriquecido con vitaminas y minerales esenciales.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros",
    "image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 17300.0,
        "margin_percent": 25.0,
        "sale_price": 21625.0,
        "list_price": 21625.0,
        "stock_qty": 50,
        "sku": "GC-CACH-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 123,
    "category_id": 2,
    "brand_id": 18,
    "name": "Gran Campeón Gato Pescado y Pollo",
    "slug": "gran-campeon-gato-10kg",
    "description": "Alimento completo para gatos adultos con sabor irresistible a pescado y pollo. Ayuda al control de bolas de pelo.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Económico Gatos",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 23300.0,
        "margin_percent": 25.0,
        "sale_price": 29125.0,
        "list_price": 29125.0,
        "stock_qty": 50,
        "sku": "GC-GAT-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 124,
    "category_id": 1,
    "brand_id": 23,
    "name": "Cooperación ACA Perro Adulto Carne / Pollo",
    "slug": "cooperacion-aca-perro-adulto-20kg",
    "description": "Elaborado por la Asociación de Cooperativas Argentinas con granos seleccionados del campo y harinas de carne de primera.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Cooperativa ACA",
    "image_url": "https://images.unsplash.com/photo-1568640347023-a616a30bc3bd?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Carne 20 kg",
        "weight_kg": 20.0,
        "cost_price": 27600.0,
        "margin_percent": 22.0,
        "sale_price": 33672.0,
        "list_price": 33672.0,
        "stock_qty": 50,
        "sku": "ACA-CARN-20",
        "is_default": 1
      },
      {
        "presentation_name": "Pollo 20 kg",
        "weight_kg": 20.0,
        "cost_price": 27600.0,
        "margin_percent": 22.0,
        "sale_price": 33672.0,
        "list_price": 33672.0,
        "stock_qty": 50,
        "sku": "ACA-POLL-20",
        "is_default": 0
      }
    ]
  },
  {
    "id": 125,
    "category_id": 1,
    "brand_id": 23,
    "name": "Cooperación ACA Cachorros",
    "slug": "cooperacion-aca-cachorros-15kg",
    "description": "Nutrición inicial para cachorros. Desarrollado con aporte balanceado de proteínas y ácidos grasos esenciales.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Cachorros ACA",
    "image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 26400.0,
        "margin_percent": 25.0,
        "sale_price": 33000.0,
        "list_price": 33000.0,
        "stock_qty": 50,
        "sku": "ACA-CACH-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 126,
    "category_id": 2,
    "brand_id": 23,
    "name": "Cooperación ACA Gato Pescado y Pollo",
    "slug": "cooperacion-aca-gato-10kg",
    "description": "Alimento completo para gatos de todas las edades con balance mineral adecuado para cuidar las vías urinarias.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Gatos ACA",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 21100.0,
        "margin_percent": 25.0,
        "sale_price": 26375.0,
        "list_price": 26375.0,
        "stock_qty": 50,
        "sku": "ACA-GAT-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 127,
    "category_id": 1,
    "brand_id": 38,
    "name": "Performance Dog Adulto Raza Mediana y Grande",
    "slug": "performance-dog-adulto",
    "description": "Nutrición Super Premium con ingredientes de altísima digestibilidad, condroitín sulfato y glucosamina para articulaciones saludables.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Super Premium",
    "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 77000.0,
        "margin_percent": 22.0,
        "sale_price": 93940.0,
        "list_price": 93940.0,
        "stock_qty": 50,
        "sku": "PERF-AD-15",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 20 kg",
        "weight_kg": 20.0,
        "cost_price": 98600.0,
        "margin_percent": 20.0,
        "sale_price": 118320.0,
        "list_price": 118320.0,
        "stock_qty": 50,
        "sku": "PERF-AD-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 128,
    "category_id": 1,
    "brand_id": 38,
    "name": "Performance Dog Cachorro Puppy",
    "slug": "performance-dog-cachorro-15kg",
    "description": "Fórmula Super Premium para cachorros. Enriquecida con DHA para un óptimo desarrollo cerebral y visual durante el crecimiento.",
    "pet_type": "perros",
    "subcat": "cachorro",
    "breed_size": "todas",
    "badge": "Super Premium",
    "image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 83200.0,
        "margin_percent": 20.0,
        "sale_price": 99840.0,
        "list_price": 99840.0,
        "stock_qty": 50,
        "sku": "PERF-CACH-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 129,
    "category_id": 1,
    "brand_id": 38,
    "name": "Performance Dog Light Control de Peso",
    "slug": "performance-dog-light-15kg",
    "description": "Nutrición calóricamente reducida con altos niveles de L-Carnitina y fibra para perros con sobrepeso o tendencia al sedentarismo.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Control de Peso",
    "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 77000.0,
        "margin_percent": 20.0,
        "sale_price": 92400.0,
        "list_price": 92400.0,
        "stock_qty": 50,
        "sku": "PERF-LIGHT-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 130,
    "category_id": 2,
    "brand_id": 38,
    "name": "Performance Cat Adulto Pollo y Arroz",
    "slug": "performance-cat-adulto-7-5kg",
    "description": "Super Premium felino formulado para mantener la masa muscular magra y prevenir la formación de cálculos de estruvita.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Super Premium",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 66000.0,
        "margin_percent": 22.0,
        "sale_price": 80520.0,
        "list_price": 80520.0,
        "stock_qty": 50,
        "sku": "PERF-CAT-7.5",
        "is_default": 1
      }
    ]
  },
  {
    "id": 131,
    "category_id": 2,
    "brand_id": 38,
    "name": "Performance Kitten Gatitos en Crecimiento",
    "slug": "performance-kitten-7-5kg",
    "description": "Fórmula especialmente diseñada para gatitos desde el destete hasta el año de edad. Refuerzo inmunológico superior.",
    "pet_type": "gatos",
    "subcat": "gatito",
    "breed_size": "todas",
    "badge": "Gatitos",
    "image_url": "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 70300.0,
        "margin_percent": 22.0,
        "sale_price": 85766.0,
        "list_price": 85766.0,
        "stock_qty": 50,
        "sku": "PERF-KIT-7.5",
        "is_default": 1
      }
    ]
  },
  {
    "id": 132,
    "category_id": 4,
    "brand_id": 39,
    "name": "Piedras Sanitarias The Best Absorbentes Clásicas",
    "slug": "piedras-sanitarias-the-best-clasica-18kg",
    "description": "Piedras absorbentes minerales naturales de granulometría media. Pack económico de 10 bolsas de 1.8 kg (total 18 kg).",
    "pet_type": "gatos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Pack x 10 Unidades",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Fardo 10 x 1.8 kg [18 kg]",
        "weight_kg": 18.0,
        "cost_price": 13400.0,
        "margin_percent": 25.0,
        "sale_price": 16750.0,
        "list_price": 16750.0,
        "stock_qty": 50,
        "sku": "TB-CLAS-18",
        "is_default": 1
      }
    ]
  },
  {
    "id": 133,
    "category_id": 4,
    "brand_id": 39,
    "name": "Piedras Sanitarias The Best Perfumadas con Fragancia Floral",
    "slug": "piedras-sanitarias-the-best-perfumada",
    "description": "Piedras sanitarias minerales con aroma floral que se activa al contacto con los líquidos, neutralizando olores al instante.",
    "pet_type": "gatos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Aroma Floral",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Fardo 10 x 1.8 kg [18 kg]",
        "weight_kg": 18.0,
        "cost_price": 15300.0,
        "margin_percent": 25.0,
        "sale_price": 19125.0,
        "list_price": 19125.0,
        "stock_qty": 50,
        "sku": "TB-PERF-18",
        "is_default": 0
      },
      {
        "presentation_name": "Fardo 6 x 3.6 kg [21.6 kg]",
        "weight_kg": 21.6,
        "cost_price": 17100.0,
        "margin_percent": 25.0,
        "sale_price": 21375.0,
        "list_price": 21375.0,
        "stock_qty": 50,
        "sku": "TB-PERF-21.6",
        "is_default": 1
      }
    ]
  },
  {
    "id": 134,
    "category_id": 4,
    "brand_id": 39,
    "name": "Piedras Sanitarias Mi Niño Absorbentes para Gatos",
    "slug": "piedras-sanitarias-mi-nino-20kg",
    "description": "Piedras minerales clásicas súper absorbentes en presentación rendidora: pack de 10 bolsas de 2 kg (total 20 kg).",
    "pet_type": "gatos",
    "subcat": "higiene",
    "breed_size": "todas",
    "badge": "Pack 20 kg",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Pack 10 x 2 kg [20 kg]",
        "weight_kg": 20.0,
        "cost_price": 12300.0,
        "margin_percent": 25.0,
        "sale_price": 15375.0,
        "list_price": 15375.0,
        "stock_qty": 50,
        "sku": "MN-PIED-20",
        "is_default": 1
      }
    ]
  },
  {
    "id": 135,
    "category_id": 2,
    "brand_id": 22,
    "name": "Chacal Gato Pescado y Carne",
    "slug": "chacal-gato-pescado-carne",
    "description": "Alimento balanceado económico para gatos con proteínas de pescado y carne vacuna. Sabor agradable y buena digestibilidad.",
    "pet_type": "gatos",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Económico Felino",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 8 kg",
        "weight_kg": 8.0,
        "cost_price": 15200.0,
        "margin_percent": 25.0,
        "sale_price": 19000.0,
        "list_price": 19000.0,
        "stock_qty": 50,
        "sku": "CHAC-GAT-8",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 27100.0,
        "margin_percent": 22.0,
        "sale_price": 33062.0,
        "list_price": 33062.0,
        "stock_qty": 50,
        "sku": "CHAC-GAT-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 136,
    "category_id": 1,
    "brand_id": 22,
    "name": "Balancín Alimento Completo para Perros",
    "slug": "balancin-perro-15kg",
    "description": "La opción más económica del mercado para alimentación canina completa de mantenimiento.",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "todas",
    "badge": "Súper Económico",
    "image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 14300.0,
        "margin_percent": 25.0,
        "sale_price": 17875.0,
        "list_price": 17875.0,
        "stock_qty": 50,
        "sku": "BAL-PERR-15",
        "is_default": 1
      }
    ]
  },
  {
    "id": 137,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Veterinary Canine Hipoalergénico",
    "slug": "royal-canin-veterinary-canine-hipoalergenico",
    "description": "Alimento dietético para perros con alergias alimentarias, intolerancias o afecciones dermatológicas y gastrointestinales crónicas.",
    "pet_type": "perros",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Dieta Veterinaria",
    "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 2 kg",
        "weight_kg": 2.0,
        "cost_price": 33600.0,
        "margin_percent": 25.0,
        "sale_price": 42000.0,
        "list_price": 42000.0,
        "stock_qty": 50,
        "sku": "RC-VET-HIP-2",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 127650.0,
        "margin_percent": 20.0,
        "sale_price": 153180.0,
        "list_price": 153180.0,
        "stock_qty": 50,
        "sku": "RC-VET-HIP-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 138,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Veterinary Canine Gastrointestinal Dog",
    "slug": "royal-canin-veterinary-canine-gastrointestinal",
    "description": "Soporte nutricional para la recuperación gastrointestinal en perros. Alta densidad energética y fibras solubles prebióticas.",
    "pet_type": "perros",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Salud Digestiva",
    "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 2 kg",
        "weight_kg": 2.0,
        "cost_price": 27500.0,
        "margin_percent": 25.0,
        "sale_price": 34375.0,
        "list_price": 34375.0,
        "stock_qty": 50,
        "sku": "RC-VET-GAST-2",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 107100.0,
        "margin_percent": 20.0,
        "sale_price": 128520.0,
        "list_price": 128520.0,
        "stock_qty": 50,
        "sku": "RC-VET-GAST-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 139,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Veterinary Canine Renal Dog",
    "slug": "royal-canin-veterinary-canine-renal",
    "description": "Dieta formulada para ayudar a la función renal en casos de insuficiencia renal crónica canina. Bajo fósforo y proteínas de alta calidad.",
    "pet_type": "perros",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Soporte Renal",
    "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 1.5 kg",
        "weight_kg": 1.5,
        "cost_price": 20500.0,
        "margin_percent": 25.0,
        "sale_price": 25625.0,
        "list_price": 25625.0,
        "stock_qty": 50,
        "sku": "RC-VET-REN-1.5",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 110000.0,
        "margin_percent": 20.0,
        "sale_price": 132000.0,
        "list_price": 132000.0,
        "stock_qty": 50,
        "sku": "RC-VET-REN-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 140,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Veterinary Canine Urinary S/O Dog",
    "slug": "royal-canin-veterinary-canine-urinary-so",
    "description": "Manejo dietético para la disolución y prevención de cálculos de estruvita y oxalato de calcio en perros adultos.",
    "pet_type": "perros",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Salud Urinaria",
    "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 1.5 kg",
        "weight_kg": 1.5,
        "cost_price": 21700.0,
        "margin_percent": 25.0,
        "sale_price": 27125.0,
        "list_price": 27125.0,
        "stock_qty": 50,
        "sku": "RC-VET-URI-1.5",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 10 kg",
        "weight_kg": 10.0,
        "cost_price": 119000.0,
        "margin_percent": 20.0,
        "sale_price": 142800.0,
        "list_price": 142800.0,
        "stock_qty": 50,
        "sku": "RC-VET-URI-10",
        "is_default": 1
      }
    ]
  },
  {
    "id": 141,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Veterinary Feline Urinary S/O Cat",
    "slug": "royal-canin-veterinary-feline-urinary-so",
    "description": "Dieta clínica específica para gatos con síndrome urológico felino (FLUTD), disolución de cálculos de estruvita y cistitis idiopática.",
    "pet_type": "gatos",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Salud Urinaria Felina",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 1.5 kg",
        "weight_kg": 1.5,
        "cost_price": 31570.0,
        "margin_percent": 25.0,
        "sale_price": 39462.0,
        "list_price": 39462.0,
        "stock_qty": 50,
        "sku": "RC-VET-CAT-URI-1.5",
        "is_default": 0
      },
      {
        "presentation_name": "Bolsa 7.5 kg",
        "weight_kg": 7.5,
        "cost_price": 116520.0,
        "margin_percent": 20.0,
        "sale_price": 139824.0,
        "list_price": 139824.0,
        "stock_qty": 50,
        "sku": "RC-VET-CAT-URI-7.5",
        "is_default": 1
      }
    ]
  },
  {
    "id": 142,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Veterinary Feline Gastrointestinal Cat",
    "slug": "royal-canin-veterinary-feline-gastrointestinal",
    "description": "Fórmula altamente digestible para gatos con trastornos gastrointestinales agudos o crónicos. Enriquecida con electrolitos.",
    "pet_type": "gatos",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Salud Digestiva Felina",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 2 kg",
        "weight_kg": 2.0,
        "cost_price": 39270.0,
        "margin_percent": 25.0,
        "sale_price": 49088.0,
        "list_price": 49088.0,
        "stock_qty": 50,
        "sku": "RC-VET-CAT-GAST-2",
        "is_default": 1
      }
    ]
  },
  {
    "id": 143,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Veterinary Feline Renal Cat",
    "slug": "royal-canin-veterinary-feline-renal",
    "description": "Soporte nutricional para la insuficiencia renal crónica felina. Muy alta palatabilidad para gatos con pérdida de apetito.",
    "pet_type": "gatos",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Soporte Renal Felino",
    "image_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Bolsa 2 kg",
        "weight_kg": 2.0,
        "cost_price": 35950.0,
        "margin_percent": 25.0,
        "sale_price": 44938.0,
        "list_price": 44938.0,
        "stock_qty": 50,
        "sku": "RC-VET-CAT-REN-2",
        "is_default": 1
      }
    ]
  },
  {
    "id": 144,
    "category_id": 5,
    "brand_id": 1,
    "name": "Royal Canin Recovery Lata Húmeda x 195 gr",
    "slug": "royal-canin-recovery-lata-195g",
    "description": "Alimento húmedo completo y de textura mousse muy suave para perros y gatos en períodos de convalecencia, postoperatorios o desnutrición.",
    "pet_type": "ambos",
    "subcat": "veterinaria",
    "breed_size": "todas",
    "badge": "Cuidados Intensivos",
    "image_url": "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=600&auto=format&fit=crop&q=80",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": null,
    "variants": [
      {
        "presentation_name": "Lata 195 gr",
        "weight_kg": 0.195,
        "cost_price": 7300.0,
        "margin_percent": 28.0,
        "sale_price": 9344.0,
        "list_price": 9344.0,
        "stock_qty": 50,
        "sku": "RC-REC-LATA-195",
        "is_default": 1
      }
    ]
  },
  {
    "id": 145,
    "category_id": 1,
    "brand_id": 1,
    "name": "Test Alimento Manual Criador",
    "slug": "test-alimento-manual-criador",
    "description": "Producto de prueba para verificar endpoint POST",
    "pet_type": "perros",
    "subcat": "adulto",
    "breed_size": "grande",
    "badge": "Nuevo",
    "image_url": "https://example.com/test.jpg",
    "is_featured": 0,
    "is_promo": 0,
    "promo_tag": "",
    "variants": [
      {
        "presentation_name": "Bolsa 15 kg",
        "weight_kg": 15.0,
        "cost_price": 50000.0,
        "margin_percent": 25.0,
        "sale_price": 62500.0,
        "list_price": 71875.0,
        "stock_qty": 50,
        "sku": "PROD-145",
        "is_default": 0
      }
    ]
  }
]

def init_db():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    for cat in CATEGORIES_DATA:
        cursor.execute(
            "INSERT INTO categories (slug, name, pet_type, icon, display_order) VALUES (?, ?, ?, ?, ?)",
            (cat['slug'], cat['name'], cat['pet_type'], cat['icon'], cat['display_order'])
        )

    for b in BRANDS_DATA:
        cursor.execute(
            "INSERT INTO brands (name, tier, origin) VALUES (?, ?, ?)",
            (b['name'], b['tier'], b['origin'])
        )

    for p in PRODUCTS_DATA:
        cursor.execute("""
            INSERT INTO products (
                id, category_id, brand_id, name, slug, description, pet_type, subcat,
                breed_size, badge, image_url, is_featured, is_promo, promo_tag, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            p['id'], p['category_id'], p['brand_id'], p['name'], p['slug'], p['description'],
            p['pet_type'], p['subcat'], p['breed_size'], p['badge'], p['image_url'],
            p['is_featured'], p['is_promo'], p['promo_tag']
        ))

        for v in p['variants']:
            cursor.execute("""
                INSERT INTO product_variants (
                    product_id, presentation_name, weight_kg, cost_price, margin_percent,
                    sale_price, list_price, stock_qty, sku, is_default
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['id'], v['presentation_name'], v['weight_kg'], v['cost_price'],
                v['margin_percent'], v['sale_price'], v['list_price'], v['stock_qty'],
                v['sku'], v['is_default']
            ))

    conn.commit()
    conn.close()
    print("Base de datos petshop.db poblada exitosamente con 144 productos y 255 presentaciones.")

if __name__ == '__main__':
    init_db()
