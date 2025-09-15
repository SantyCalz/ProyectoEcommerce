from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import Producto, Carrito, CarritoProducto, Categoria, Pedido, PedidoProducto
from .forms import RegistroForm, UsuarioChangeForm
import mercadopago
from django.conf import settings
from django.http import HttpResponse


# Vista principal de "Mi Cuenta"
@login_required
def mi_cuenta(request):
    return render(request, 'productos/mi_cuenta.html')


# Vista para editar datos del usuario
@login_required
def editar_datos_usuario(request):
    user = request.user
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('mi_cuenta')
    else:
        form = UsuarioChangeForm(instance=user)
        password_form = PasswordChangeForm(user)
    return render(request, 'productos/editar_datos_usuario.html', {'form': form, 'password_form': password_form})


# Vista para historial de compras
@login_required
def historial_compras(request):
    pedidos = request.user.pedido_set.order_by('-fecha').all()
    return render(request, 'productos/historial_compras.html', {'pedidos': pedidos})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


def lista_productos(request):
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')

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
def vaciar_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.carritoproducto_set.all().delete()
    return redirect('ver_carrito')




from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .models import Carrito, Pedido, PedidoProducto, Producto

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Carrito, Pedido, PedidoProducto, Producto

@login_required
def checkout(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    total = carrito.total()

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        direccion = request.POST.get('direccion', '')

        # Guardar la dirección en session para usarla luego
        request.session['direccion_envio'] = direccion

        # Inicializar SDK de Mercado Pago
        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

        # Armar items según el carrito
        items = []
        for item in carrito.carritoproducto_set.all():
            items.append({
                "title": item.producto.nombre,
                "quantity": item.cantidad,
                "unit_price": float(item.producto.precio),
                "currency_id": "ARS",
            })

        preference_data = {
            "items": items,
            "payer": {"email": request.user.email},
            "back_urls": {
                "success": request.build_absolute_uri("/checkout/success/manual/"),
                "failure": request.build_absolute_uri("/checkout/failure/"),
                "pending": request.build_absolute_uri("/checkout/pending/"),
            },
            # "auto_return": "approved",
        }

        try:
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response.get("response", {})

            print("=== Respuesta completa de Mercado Pago ===")
            print(preference_response)
            print("=== URL sandbox que se intentará enviar al frontend ===")
            print(preference.get("sandbox_init_point"))

            url = preference.get("sandbox_init_point")
            if not url:
                return HttpResponse("Error")
            return HttpResponse(url)
        except Exception as e:
            print("Error al crear preferencia de Mercado Pago:", e)
            return HttpResponse("Error")

    return render(request, 'productos/checkout.html', {'carrito': carrito, 'total': total})


@login_required
def pago_aprobado(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    direccion = request.session.get('direccion_envio', '')  # Tomamos la dirección de la session

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            if not carrito.carritoproducto_set.exists():
                return JsonResponse({'status': 'error', 'message': 'No hay productos en el carrito.'})

            pedido = Pedido.objects.create(
                usuario=request.user,
                total=carrito.total(),
                pagado=True,
                direccion_envio=direccion  # Guardamos la dirección aquí
            )

            for item in carrito.carritoproducto_set.all():
                PedidoProducto.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio
                )
                producto = item.producto
                producto.stock -= item.cantidad
                if producto.stock < 0:
                    producto.stock = 0
                producto.save()

            carrito.carritoproducto_set.all().delete()

            # Limpiar dirección de la session
            if 'direccion_envio' in request.session:
                del request.session['direccion_envio']

            return JsonResponse({'status': 'ok', 'message': 'Pedido generado correctamente.'})

        except Exception as e:
            print("Error en pago_aprobado:", e)
            return JsonResponse({'status': 'error', 'message': 'Ocurrió un error al generar el pedido. Intenta nuevamente.'})

    # GET → mostrar la página con botón
    return render(request, "productos/pago_aprobado.html", {'carrito': carrito})


@login_required
def checkout_success_manual(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if not carrito.carritoproducto_set.exists():
        return redirect('lista_productos')

    pedido = Pedido.objects.create(usuario=request.user, pagado=True, total=carrito.total())

    for item in carrito.carritoproducto_set.all():
        PedidoProducto.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
        )
        producto = item.producto
        producto.stock -= item.cantidad
        if producto.stock < 0:
            producto.stock = 0
        producto.save()

    carrito.carritoproducto_set.all().delete()

    return render(request, "productos/checkout_success.html")


    # Vaciar carrito
    carrito.carritoproducto_set.all().delete()

    # Redirigir a la página principal de la tienda
    return redirect('lista_productos')

@login_required
def checkout_failure(request):
    return render(request, "productos/checkout_failure.html")


@login_required
def checkout_pending(request):
    # Si querés, podés guardar que el pago está en estado "pendiente"
    return render(request, "productos/checkout_pending.html")


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
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'productos/historial.html', {'pedidos': pedidos})
