from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)                            # Nombre del producto
    descripcion = models.TextField()                                     # Descripción larga
    precio = models.DecimalField(max_digits=10, decimal_places=2)        # Precio
    stock = models.PositiveIntegerField(default=0)                       # Cantidad disponible
    creado = models.DateTimeField(auto_now_add=True)                     # Fecha de creación

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
