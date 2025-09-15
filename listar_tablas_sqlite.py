# -*- coding: utf-8 -*-

# cargar_productos_prueba.py
import random
from productos.models import Producto, Fabricante

# Lista de fabricantes de prueba
fabricantes_nombres = ["Acme Corp", "Globex", "Initech", "Umbrella", "Cyberdyne"]

# Crear fabricantes si no existen
fabricantes = []
for nombre in fabricantes_nombres:
    fab, _ = Fabricante.objects.get_or_create(nombre=nombre)
    fabricantes.append(fab)

# Lista de nombres de productos de prueba
nombres_productos = [
    "Auriculares Bluetooth",
    "Mouse Gamer",
    "Teclado Mecánico",
    "Monitor LED 24''",
    "Silla Ergonómica",
    "Notebook 15''",
    "Disco SSD 1TB",
    "Impresora Multifunción",
    "Parlante Portátil",
    "Smartwatch Deportivo",
]

# Crear productos
for nombre in nombres_productos:
    precio = round(random.uniform(10000, 150000), 2)  # Precio aleatorio
    stock = random.randint(5, 50)  # Stock aleatorio
    fabricante = random.choice(fabricantes)

    producto, created = Producto.objects.get_or_create(
        nombre=nombre,
        defaults={
            "precio": precio,
            "stock": stock,
            "fabricante": fabricante,
        }
    )

    if created:
        print(f"✅ Producto creado: {producto.nombre} (${producto.precio}, stock {producto.stock})")
    else:
        print(f"⚠️ Ya existía: {producto.nombre}")
