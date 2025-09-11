from django.contrib import admin
from .models import Producto, Categoria, Carrito, CarritoProducto

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
