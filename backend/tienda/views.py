from django.shortcuts import render, redirect, get_object_or_404
from transbank.webpay.webpay_plus.transaction import Transaction
from django.http import HttpResponse
from django.urls import reverse
import uuid


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

def agregar_al_carrito(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    carrito = request.session.get('carrito', {})

    if str(libro_id) in carrito:
        carrito[str(libro_id)]['cantidad'] += 1
    else:
        carrito[str(libro_id)] = {
            'titulo': libro.titulo,
            'precio': float(libro.precio),
            'cantidad': 1,
            'imagen': libro.imagen.url if libro.imagen else None,
        }

    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect('libros')

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