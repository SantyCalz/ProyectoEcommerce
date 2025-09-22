# ======================================================
# Imports necesarios para el admin de Django
# ======================================================
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Importación de modelos y formularios personalizados
from .models import (
    Producto, Categoria, Carrito, CarritoProducto, 
    ProductoImagen, Usuario, Pedido, PedidoProducto
)
from .forms import UsuarioCreationForm

# ======================================================
# Registro de categorías
# ======================================================
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cantidad_productos")
    search_fields = ("nombre",)

    def cantidad_productos(self, obj):
        return obj.productos.count()
    cantidad_productos.short_description = "Cantidad de productos"

admin.site.register(Categoria, CategoriaAdmin)

# ======================================================
# Inline para imágenes adicionales de productos
# ======================================================
class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ["imagen"]
    # Eliminamos preview
    # readonly_fields = ["preview"]

admin.site.register(ProductoImagenInline)

# ======================================================
# Admin de Producto
# ======================================================
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock", "categoria")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria", "stock")
    inlines = [ProductoImagenInline]

    fieldsets = (
        ("Información básica", {
            "fields": ("nombre", "descripcion", "categoria")
        }),
        ("Precio y stock", {
            "fields": ("precio", "descuento", "stock")
        }),
        ("Imagen principal", {
            "fields": ("imagen",)  # Quitamos imagen_principal_preview
        }),
        ("Imágenes adicionales", {
            "fields": (),
            "description": "Agregar imágenes adicionales en la sección de abajo"
        }),
    )

    # Eliminamos readonly_fields
    # readonly_fields = ("imagen_principal_preview",)

admin.site.register(Producto, ProductoAdmin)

# ======================================================
# Admin de Carrito
# ======================================================
class CarritoProductoInline(admin.TabularInline):
    model = CarritoProducto
    extra = 0
    readonly_fields = ("subtotal",)
    fields = ("producto", "cantidad", "subtotal")

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Subtotal"

class CarritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "total_carrito", "num_productos", "creado")
    search_fields = ("usuario__username", "usuario__email")
    list_filter = ("creado",)
    inlines = [CarritoProductoInline]

    def total_carrito(self, obj):
        return obj.total()
    total_carrito.short_description = "Total"

    def num_productos(self, obj):
        return obj.carritoproducto_set.count()
    num_productos.short_description = "N° productos"

admin.site.register(Carrito, CarritoAdmin)

# ======================================================
# Admin de CarritoProducto
# ======================================================
class CarritoProductoAdmin(admin.ModelAdmin):
    list_display = ("producto", "cantidad", "carrito", "usuario_del_carrito", "subtotal")
    search_fields = ("producto__nombre", "carrito__usuario__username")
    list_filter = ("carrito__usuario",)

    def usuario_del_carrito(self, obj):
        return obj.carrito.usuario.username
    usuario_del_carrito.short_description = "Usuario"

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Subtotal"

admin.site.register(CarritoProducto, CarritoProductoAdmin)

# ======================================================
# Admin de Pedido
# ======================================================
class PedidoProductoInline(admin.TabularInline):
    model = PedidoProducto
    extra = 0
    readonly_fields = ("precio_unitario", "subtotal")
    fields = ("producto", "cantidad", "precio_unitario", "subtotal")

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Subtotal"

class PedidoAdmin(admin.ModelAdmin):
    list_display = ("numero_pedido_formateado", "usuario", "fecha", "total", "pagado")
    search_fields = ("usuario__username", "usuario__email")
    list_filter = ("fecha", "pagado")
    inlines = [PedidoProductoInline]

    readonly_fields = ("numero_pedido_formateado", "total")

admin.site.register(Pedido, PedidoAdmin)

# ======================================================
# Admin de PedidoProducto
# ======================================================
class PedidoProductoAdmin(admin.ModelAdmin):
    list_display = ("producto", "cantidad", "precio_unitario", "pedido", "usuario_del_pedido", "subtotal")
    search_fields = ("producto__nombre", "pedido__usuario__username")
    list_filter = ("pedido__usuario",)

    def usuario_del_pedido(self, obj):
        return obj.pedido.usuario.username
    usuario_del_pedido.short_description = "Usuario"

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Subtotal"

admin.site.register(PedidoProducto, PedidoProductoAdmin)

# ======================================================
# Admin personalizado para Usuario
# ======================================================
class CustomUserAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    model = Usuario

    list_display = ["username", "email", "telefono", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "email", "telefono")}),
        ("Permisos", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "email", "telefono", 
                       "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

admin.site.register(Usuario, CustomUserAdmin)
