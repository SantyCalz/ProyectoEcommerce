from productos.models import Producto, Categoria

# Crear una categoría genérica si no existe
categoria, _ = Categoria.objects.get_or_create(nombre="Genérica")

for i in range(1, 11):
    Producto.objects.create(
        nombre=f"Producto Genérico {i}",
        descripcion=f"Descripción de prueba para el producto {i}.",
        precio=100 + i * 10,
        descuento=0,
        stock=50,
        categoria=categoria
    )

print("¡10 productos genéricos creados exitosamente!")
