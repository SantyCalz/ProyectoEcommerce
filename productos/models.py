from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)                            # Nombre del producto
    descripcion = models.TextField()                                     # Descripción larga
    precio = models.DecimalField(max_digits=10, decimal_places=2)        # Precio
    stock = models.PositiveIntegerField(default=0)                       # Cantidad disponible
    creado = models.DateTimeField(auto_now_add=True)                     # Fecha de creación
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Campo de imagen
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos", null=True, blank=True)

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoProducto', blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        total = sum(item.subtotal() for item in self.carritoproducto_set.all())
        return total

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class CarritoProducto(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


from django.db import models
from django.contrib.auth.models import User

# ... tus modelos existentes (Producto, Carrito, CarritoProducto, Categoria) ...

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField('Producto', through='PedidoProducto')
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    

