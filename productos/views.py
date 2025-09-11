from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Producto, Carrito, CarritoProducto, Categoria
from .forms import RegistroForm
from .models import Pedido, PedidoProducto



def lista_productos(request):
    query = request.GET.get('q')  # texto buscador
    categoria_id = request.GET.get('categoria')  # id de categoría seleccionada

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'categorias': categorias,
    })


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if producto.stock <= 0:
        # Podrías mostrar un mensaje de "Agotado"
        return redirect('lista_productos')

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_producto, created = CarritoProducto.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )
    if not created:
        if carrito_producto.cantidad < producto.stock:
            carrito_producto.cantidad += 1
            carrito_producto.save()
    return redirect('ver_carrito')


@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    total = carrito.total()
    return render(request, 'productos/carrito.html', {'carrito': carrito, 'total': total})


@login_required
def eliminar_del_carrito(request, producto_id):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.productos.remove(producto)
    return redirect('ver_carrito')


@login_required
def checkout(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    total = carrito.total()

    if request.method == 'POST':
        direccion = request.POST.get('direccion', '')

        # Crear pedido
        pedido = Pedido.objects.create(usuario=request.user, total=total, direccion_envio=direccion)
        
        # Agregar productos al pedido y descontar stock
        for item in carrito.carritoproducto_set.all():
            # Crear detalle de pedido
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad
            )
            
            # Descontar stock
            item.producto.stock -= item.cantidad
            item.producto.save()

        carrito.carritoproducto_set.all().delete()  # Vacía el carrito
        return render(request, 'productos/gracias.html', {'pedido': pedido})

    return render(request, 'productos/checkout.html', {'carrito': carrito, 'total': total})



def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('lista_productos')
    else:
        form = RegistroForm()
    return render(request, 'productos/registro.html', {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('lista_productos')
    else:
        form = AuthenticationForm()
    return render(request, 'productos/login.html', {'form': form})


@login_required
def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')


@login_required
def vaciar_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.carritoproducto_set.all().delete()
    return redirect('ver_carrito')


@login_required
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'productos/historial.html', {'pedidos': pedidos})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if producto.stock <= 0:
        # Producto agotado, redirigir y opcionalmente mostrar mensaje
        return redirect('lista_productos')

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_producto, created = CarritoProducto.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )

    if not created:
        if carrito_producto.cantidad < producto.stock:
            carrito_producto.cantidad += 1
            carrito_producto.save()
    return redirect('ver_carrito')
