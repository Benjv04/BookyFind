from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction
from django.http import HttpResponse


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
    response = transaction.create(
        buy_order='orden1234',
        session_id='session1234',
        amount=40000,
        return_url='http://localhost:8000/pago/exito/'
    )

    # Esto genera un formulario que se envía automáticamente vía POST a Webpay
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