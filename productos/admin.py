from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Producto, Carrito

admin.site.register(Producto)
admin.site.register(Carrito)
