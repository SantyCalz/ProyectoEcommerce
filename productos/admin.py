from django.contrib import admin
from .models import Producto, Categoria, Carrito, CarritoProducto, ProductoImagen


admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ["imagen"]
    readonly_fields = []

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock", "categoria")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria",)
    inlines = [ProductoImagenInline]


admin.site.register(Producto, ProductoAdmin)