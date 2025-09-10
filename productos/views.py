from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Carrito, CarritoProducto
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def lista_productos(request):
    productos = Producto.objects.all()                                              # Obtener todos los productos desde la base de datos            
    return render(request, 'productos/lista.html', {'productos': productos})


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    # Obtenemos o creamos el carrito del usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.productos.add(producto)
    return redirect('ver_carrito')  # Redirige a la página del carrito

@login_required
@login_required
def ver_carrito(request):
    # Obtenemos o creamos el carrito del usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    # Calculamos el total usando el método del modelo
    total = carrito.total()
    
    # Pasamos el carrito completo al template
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
        # Aquí podrías agregar lógica de pago
        carrito.carritoproducto_set.all().delete()  # Vacía el carrito
        return render(request, 'productos/gracias.html')
    
    return render(request, 'productos/checkout.html', {'carrito': carrito, 'total': total})




def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # loguea automáticamente al usuario
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
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    carrito_producto, created = CarritoProducto.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )
    if not created:
        carrito_producto.cantidad += 1
        carrito_producto.save()

    return redirect('ver_carrito')



@login_required
def vaciar_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.carritoproducto_set.all().delete()
    return redirect('ver_carrito')
