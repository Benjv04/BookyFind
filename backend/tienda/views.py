from django.shortcuts import render, redirect, get_object_or_404
from transbank.webpay.webpay_plus.transaction import Transaction
from django.http import HttpResponse
from django.urls import reverse
import uuid
from .models import Libro, Usuario
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import UsuarioCreationForm, ProductoForm
from django import forms



# Instanciar una vez
transaction = Transaction()

# Vistas de navegación
def index(request):
    return render(request, 'index.html')

def libros(request):
    return render(request, 'libros.html')

def ofertas(request):
    return render(request, 'ofertas.html')

def contacto(request):
    return render(request, 'contacto.html')

def clubes(request):
    return render(request, 'clubes.html')

def carrito(request):
    return render(request, 'carrito.html')

# Vista para iniciar el pago con Transbank
def iniciar_pago(request):
    carrito = request.session.get("carrito", {})

    if not carrito:
        return redirect("carrito")  # Redirige si no hay productos

    total = sum(int(item["precio"]) * int(item["cantidad"]) for item in carrito.values())

    # Genera identificadores únicos
    buy_order = str(uuid.uuid4())[:12]
    session_id = str(uuid.uuid4())
    return_url = request.build_absolute_uri(reverse("pago_exito"))

    response = transaction.create(
        buy_order=buy_order,
        session_id=session_id,
        amount=total,
        return_url=return_url
    )

    return HttpResponse(f"""
        <html>
            <body>
                <form id="webpay-form" action="{response['url']}" method="POST">
                    <input type="hidden" name="token_ws" value="{response['token']}">
                </form>
                <script>
                    document.getElementById('webpay-form').submit();
                </script>
            </body>
        </html>
    """)

# Vista para manejar el éxito del pago

from django.views.decorators.csrf import csrf_exempt

transaction = Transaction()

def pago_exito(request):
    token = request.POST.get('token_ws') or request.GET.get('token_ws')
    if not token:
        return redirect('pago_error')

    try:
        response = transaction.commit(token)
        # Verifica si fue aprobado
        if response['status'] == 'AUTHORIZED' or response['response_code'] == 0:
            # ✅ Vaciar carrito
            if 'carrito' in request.session:
                del request.session['carrito']
                request.session.modified = True

            return render(request, 'pago_exito.html', {'respuesta': response})
        else:
            return redirect('pago_error')
    except Exception as e:
        print(f"Error al confirmar transacción: {e}")
        return redirect('pago_error')
    
@csrf_exempt
def pago_error(request):
    return render(request, 'pago_error.html')


from django.shortcuts import render
from .models import Libro

def libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros.html', {'libros': libros})


def ofertas(request):
    # Obtener todos los libros que están en oferta
    libros_en_oferta = Libro.objects.filter(oferta=True)

    # Pasar los libros al contexto
    return render(request, 'ofertas.html', {'libros_en_oferta': libros_en_oferta})


def agregar_al_carrito(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    carrito = request.session.get('carrito', {})

    # Usar el precio con descuento si el libro está en oferta, de lo contrario, usar el precio normal
    precio_libro = libro.precio_oferta if libro.oferta else libro.precio

    # Verificar si el libro ya está en el carrito
    if str(libro_id) in carrito:
        carrito[str(libro_id)]['cantidad'] += 1
    else:
        # Agregar el libro al carrito con el precio correcto
        carrito[str(libro_id)] = {
            'titulo': libro.titulo,
            'precio': float(precio_libro),  # Asegúrate de guardar el precio correcto
            'cantidad': 1,
            'imagen': libro.imagen.url if libro.imagen else None,
        }

    # Guardar los cambios en la sesión
    request.session['carrito'] = carrito
    request.session.modified = True

    # Redirigir al usuario donde estaba (en este caso a la página de libros)
    return redirect(request.META.get('HTTP_REFERER', 'libros'))


def carrito_view(request):
    carrito = request.session.get("carrito", {})
    total = sum(float(item["precio"]) * item["cantidad"] for item in carrito.values())
    return render(request, "carrito.html", {
        "total_carrito": total,
    })

def modificar_cantidad(request, producto_id, accion):
    carrito = request.session.get("carrito", {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        if accion == 'sumar':
            carrito[producto_id]['cantidad'] += 1
        elif accion == 'restar':
            if carrito[producto_id]['cantidad'] > 1:
                carrito[producto_id]['cantidad'] -= 1
            else:
                del carrito[producto_id]  # Eliminar si la cantidad baja de 1

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect('carrito')

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        del carrito[producto_id]

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect('carrito')

def carrito_view(request):
    carrito = request.session.get("carrito", {})
    total = sum(int(item["precio"]) * int(item["cantidad"]) for item in carrito.values())
    return render(request, "carrito.html", {"total_carrito": total})


from .models import Libro

def index(request):
    libros_destacados = Libro.objects.all()[:4]
    return render(request, 'index.html', {'libros_destacados': libros_destacados})


#TODO LO DE CREAR EL LOGIN

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, "Tu cuenta ha sido creada correctamente. Ya puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = UsuarioCreationForm()
    return render(request, 'cuenta/registro.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('cuenta')

    libros = Libro.objects.all()
    usuarios = Usuario.objects.filter(is_staff=False)  # Mostrar solo usuarios no administradores

    return render(request, 'cuenta/admin_panel.html', {
        'libros': libros,
        'usuarios': usuarios
    })



@require_POST
def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}.")

            # Redirige según si es staff o no
            if user.is_staff:
                return redirect('admin_panel')
            else:
                return redirect('cuenta')
        else:
            messages.error(request, "Credenciales inválidas.")
    else:
        form = AuthenticationForm()
    return render(request, 'cuenta/login.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_productos(request):
    libros = Libro.objects.all()
    return render(request, 'cuenta/admin_productos.html', {'libros': libros})

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'descripcion', 'precio', 'precio_oferta', 'oferta', 'stock', 'imagen']

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_producto(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ProductoForm(instance=libro)

    return render(request, 'cuenta/editar_producto.html', {'form': form, 'libro': libro})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_usuarios(request):
    Usuario = get_user_model()  # Asegura que estás usando el modelo personalizado
    usuarios = Usuario.objects.all()  # Sin filtro
    return render(request, 'cuenta/admin_usuarios.html', {'usuarios': usuarios})

@login_required
def cuenta_view(request):
    return render(request, 'cuenta/cuenta.html')

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def eliminar_usuario(request, usuario_id):
    Usuario = get_user_model()
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if usuario.is_staff:
        messages.error(request, "No puedes eliminar a otro administrador.")
    else:
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")

    return redirect('admin_panel')