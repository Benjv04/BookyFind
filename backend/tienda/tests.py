# tests.py - Pruebas Unitarias para BookyFind
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from unittest.mock import Mock, patch
from decimal import Decimal
from .models import Libro

User = get_user_model()

class GestionUsuariosTestCase(TestCase):
    """
    8.1. Componente: Gestión de Usuarios
    """
    
    def setUp(self):
        """Configuración inicial para pruebas de usuarios"""
        self.client = Client()
        
        # Usuario existente para pruebas de duplicados
        self.usuario_existente = User.objects.create_user(
            username='benj.gonzalezn@duocuc.cl',
            email='benj.gonzalezn@duocuc.cl',
            password='Contraseña123'
        )
    
    def test_creacion_usuario_datos_validos(self):
        """
        Prueba 1: Creación de usuario con datos válidos
        
        Descripción clara de la prueba:
        Se verificará que el sistema permita la creación de un nuevo usuario al ingresar datos válidos.
        
        Código involucrado:
        Vista: registro_usuario()
        Formulario: UsuarioCreationForm
        Template: cuenta/registro.html
        """
        # Ejecución de la prueba:
        datos_validos = {
            'username': 'ejemplo1@duocuc.cl',
            'email': 'ejemplo1@duocuc.cl',
            'password1': 'Contraseña123',
            'password2': 'Contraseña123'
        }
        
        response = self.client.post(reverse('registro'), datos_validos)
        
        # Captura del resultado:
        # Verificar redirección exitosa a login
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario fue creado
        usuario_creado = User.objects.filter(username='ejemplo1@duocuc.cl').exists()
        self.assertTrue(usuario_creado)
        
        # Verificar mensaje de éxito
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any("cuenta ha sido creada correctamente" in str(m) for m in messages_list))
        
        # Análisis del resultado:
        print("Prueba realizada con éxito - Usuario creado correctamente")
    
    def test_login_credenciales_incorrectas(self):
        """
        Prueba 2: Intento de inicio de sesión con credenciales incorrectas
        
        Descripción clara de la prueba:
        Confirmar que el sistema rechace intentos de inicio de sesión con contraseñas incorrectas.
        
        Código involucrado:
        Vista: login_view()
        Formulario: AuthenticationForm
        Template: cuenta/login.html
        """
        # Ejecución de la prueba:
        datos_incorrectos = {
            'username': 'benj.gonzalezn@duocuc.cl',  # Usuario existente
            'password': 'ContraseñaIncorrecta123'    # Contraseña incorrecta
        }
        
        response = self.client.post(reverse('login'), datos_incorrectos)
        
        # Captura del resultado:
        # Verificar que no se redirige (se queda en la página de login)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el usuario no está autenticado
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        
        # Verificar mensaje de error
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any("Credenciales inválidas" in str(m) for m in messages_list))
        
        # Análisis del resultado:
        print("Prueba realizada con éxito - Login rechazado correctamente")
    
    def test_registro_email_duplicado(self):
        """
        Prueba 3: Registro con correo electrónico ya existente
        
        Descripción clara de la prueba:
        Verificar que el sistema no permita registrar usuarios con emails duplicados.
        
        Código involucrado:
        Vista: registro_usuario()
        Formulario: UsuarioCreationForm (validación unique)
        Template: cuenta/registro.html
        """
        # Ejecución de la prueba:
        datos_duplicados = {
            'username': 'benj.gonzalezn@duocuc.cl',  # Email ya existente
            'email': 'benj.gonzalezn@duocuc.cl',
            'password1': 'Contraseña123',
            'password2': 'Contraseña123'
        }
        
        response = self.client.post(reverse('registro'), datos_duplicados)
        
        # Captura del resultado:
        # Verificar que no se redirige (se queda en registro con errores)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que no se creó un nuevo usuario
        usuarios_count = User.objects.filter(username='benj.gonzalezn@duocuc.cl').count()
        self.assertEqual(usuarios_count, 1)  # Solo el usuario original
        
        # Verificar que aparecen errores del formulario
        self.assertContains(response, 'error')
        
        # Análisis del resultado:
        print("Prueba realizada con éxito - Sistema previene duplicados de email")


from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Libro
from django.core.files.base import ContentFile
from io import BytesIO

class CatalogoLibrosTestCase(TestCase):
    """
    8.2. Componente: Catálogo de Libros
    """
    
    def setUp(self):
        """Configuración inicial para pruebas de catálogo"""
        self.client = Client()
        
        # Crear libros de prueba con una imagen predeterminada (o vacía)
        # Usamos una imagen ficticia en formato byte
        image_file = BytesIO(b"fake image content")
        image_file.name = 'test_image.jpg'
        
        self.libro1 = Libro.objects.create(
            titulo="El Quijote",
            autor="Miguel de Cervantes",
            editorial="Editorial Planeta",
            descripcion="Novela clásica española",
            precio=Decimal('15000'),
            stock=10,
            oferta=False,
            imagen=ContentFile(image_file.read(), name='test_image.jpg')  # Asignar imagen
        )
        
        self.libro2 = Libro.objects.create(
            titulo="Cien años de soledad",
            autor="Gabriel García Márquez",
            editorial="Editorial Sudamericana",
            descripcion="Realismo mágico",
            precio=Decimal('20000'),
            precio_oferta=Decimal('15000'),
            stock=5,
            oferta=True,
            imagen=ContentFile(image_file.read(), name='test_image.jpg')  # Asignar imagen
        )
        
        self.libro3 = Libro.objects.create(
            titulo="1984",
            autor="George Orwell",
            editorial="Editorial Planeta",
            descripcion="Distopía clásica",
            precio=Decimal('18000'),
            stock=8,
            imagen=ContentFile(image_file.read(), name='test_image.jpg')  # Asignar imagen
        )
    
    def test_visualizacion_libros_disponibles(self):
        """
        Prueba 1: Visualización de libros disponibles
        
        Descripción clara de la prueba:
        Confirmar la correcta visualización de todos los libros activos en la plataforma.
        
        Código involucrado:
        Vista: libros()
        Template: libros.html
        Bucle: {% for libro in libros %}
        Cards con título, precio, imagen y botón agregar al carrito
        """
        # Ejecución de la prueba:
        response = self.client.get(reverse('libros'))
        
        # Captura del resultado:
        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verificar que todos los libros estén presentes
        self.assertContains(response, "El Quijote")
        self.assertContains(response, "Cien años de soledad")
        self.assertContains(response, "1984")
        
        # Verificar elementos requeridos para cada libro
        self.assertContains(response, "$15000")  # Precio libro1
        self.assertContains(response, "$18000")  # Precio libro3
        self.assertContains(response, "Agregar al carrito", count=6)  # 3 en cards + 3 en modales
        
        # Análisis del resultado:
        print("✅ Todos los libros de la base de datos están en la vista")
    
    def test_visualizar_detalle_libros_modal(self):
        """
        Prueba 2: Visualizar detalle de libros
        
        Descripción clara de la prueba:
        Validar que se pueda ver detalle de los libros en modales con información completa.
        
        Código involucrado:
        Template: libros.html
        Modal: modalLibro{{ libro.id }}
        Campos: autor, editorial, fecha_publicacion, descripcion
        """
        # Ejecución de la prueba:
        response = self.client.get(reverse('libros'))
        content = response.content.decode()
        
        # Captura del resultado:
        # Verificar que existen los modales
        self.assertIn(f'modalLibro{self.libro1.id}', content)
        self.assertIn(f'modalLibro{self.libro2.id}', content)
        
        # Verificar información detallada en modales
        self.assertContains(response, "Miguel de Cervantes")
        self.assertContains(response, "Editorial Planeta")
        self.assertContains(response, "Gabriel García Márquez")
        self.assertContains(response, "Novela clásica española")
        
        # Análisis del resultado:
        print("✅ Los modales muestran correctamente toda la información detallada")
    
    def test_libros_con_oferta_precio_correcto(self):
        """
        Prueba 3: Búsqueda y filtrado por ofertas
        
        Descripción clara de la prueba:
        Validar que los libros en oferta muestren correctamente ambos precios y el ícono de oferta.
        
        Código involucrado:
        Template: libros.html
        Condicional: {% if libro.oferta and libro.precio_oferta %}
        Elementos: <del>${{ libro.precio }}</del> y precio_oferta
        Imagen: oferta_png.png
        """
        # Ejecución de la prueba:
        response = self.client.get(reverse('libros'))
        content = response.content.decode()
        
        # Captura del resultado:
        # Verificar precio original tachado y precio de oferta
        self.assertIn('<del>$20000</del>', content)
        self.assertIn('$15000', content)
        
        # Verificar ícono de oferta
        self.assertIn('oferta_png.png', content)
        
        # Verificar que libro sin oferta no tiene precio tachado
        self.assertNotIn('<del>$15000</del>', content)  # El Quijote no tiene oferta
        
        # Análisis del resultado:
        print("Sistema muestra correctamente precios de oferta y precios normales")


class CarritoComprasTestCase(TestCase):
    """
    8.3. Componente: Carrito de Compras
    """
    
    def setUp(self):
        """Configuración inicial para pruebas de carrito"""
        self.client = Client()
        
        self.libro = Libro.objects.create(
            titulo="Libro de Prueba Carrito",
            autor="Autor Test",
            precio=Decimal('12000'),
            stock=10
        )
        
        self.libro_oferta = Libro.objects.create(
            titulo="Libro Oferta Carrito",
            autor="Autor Test",
            precio=Decimal('25000'),
            precio_oferta=Decimal('18000'),
            oferta=True,
            stock=5
        )
    
    def test_agregar_libro_al_carrito(self):
        """
        Prueba 1: Agregar libro al carrito
        
        Descripción clara de la prueba:
        Verificar que un libro pueda añadirse correctamente al carrito desde la vista de libros.
        
        Código involucrado:
        Vista: agregar_al_carrito()
        Form: POST a {% url 'agregar_al_carrito' libro.id %}
        Sesión: request.session['carrito']
        """
        # Ejecución de la prueba:
        response = self.client.post(
            reverse('agregar_al_carrito', args=[self.libro.id])
        )
        
        # Captura del resultado:
        # Verificar redirección exitosa
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el libro está en la sesión
        session = self.client.session
        carrito = session.get('carrito', {})
        
        self.assertIn(str(self.libro.id), carrito)
        item = carrito[str(self.libro.id)]
        
        # Verificar datos correctos del item
        self.assertEqual(item['titulo'], "Libro de Prueba Carrito")
        self.assertEqual(item['precio'], 12000.0)
        self.assertEqual(item['cantidad'], 1)
        
        # Análisis del resultado:
        print("✅ Libro agregado correctamente al carrito con todos sus datos")
    
    def test_eliminar_libro_del_carrito(self):
        """
        Prueba 2: Eliminar libro del carrito
        
        Descripción clara de la prueba:
        Comprobar que un libro pueda eliminarse completamente del carrito.
        
        Código involucrado:
        Vista: eliminar_del_carrito()
        Form: POST a {% url 'eliminar_del_carrito' key %}
        Botón: "Eliminar" en template carrito.html
        """
        # Ejecución de la prueba:
        # Primero agregar libro al carrito
        self.client.post(reverse('agregar_al_carrito', args=[self.libro.id]))
        
        # Luego eliminarlo
        response = self.client.post(
            reverse('eliminar_del_carrito', args=[self.libro.id])
        )
        
        # Captura del resultado:
        # Verificar redirección
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el libro ya no está en el carrito
        session = self.client.session
        carrito = session.get('carrito', {})
        self.assertNotIn(str(self.libro.id), carrito)
        
        # Verificar que el carrito queda vacío
        self.assertEqual(len(carrito), 0)
        
        # Análisis del resultado:
        print("✅ Libro eliminado correctamente del carrito")
    
    def test_modificar_cantidad_en_carrito(self):
        """
        Prueba 3: Modificar cantidad en el carrito
        
        Descripción clara de la prueba:
        Validar que la cantidad de un producto pueda modificarse usando los botones + y -.
        
        Código involucrado:
        Vista: modificar_cantidad()
        Forms: POST a {% url 'modificar_cantidad' key 'sumar' %}
        Botones: "+" y "-" en template carrito.html
        """
        # Ejecución de la prueba:
        # Agregar libro al carrito
        self.client.post(reverse('agregar_al_carrito', args=[self.libro.id]))
        
        # Aumentar cantidad (botón +)
        response = self.client.post(
            reverse('modificar_cantidad', args=[self.libro.id, 'sumar'])
        )
        
        # Verificar aumento de cantidad
        session = self.client.session
        carrito = session.get('carrito', {})
        self.assertEqual(carrito[str(self.libro.id)]['cantidad'], 2)
        
        # Disminuir cantidad (botón -)
        self.client.post(
            reverse('modificar_cantidad', args=[self.libro.id, 'restar'])
        )
        
        # Captura del resultado:
        session = self.client.session
        carrito = session.get('carrito', {})
        self.assertEqual(carrito[str(self.libro.id)]['cantidad'], 1)
        
        # Análisis del resultado:
        print("✅ Cantidad modificada correctamente usando botones + y -")


class PedidosPagosTestCase(TestCase):
    """
    8.4. Componente: Pedidos y Pagos
    """
    
    def setUp(self):
        """Configuración inicial para pruebas de pagos"""
        self.client = Client()
        
        self.libro = Libro.objects.create(
            titulo="Libro Pago Test",
            autor="Autor Test",
            editorial="Editorial Test",
            descripcion="Descripción test",
            precio=Decimal('30000'),
            stock=10
        )
        
        self.libro_oferta = Libro.objects.create(
            titulo="Libro Oferta Test",
            autor="Autor Test",
            editorial="Editorial Test",
            descripcion="Descripción test oferta",
            precio=Decimal('25000'),
            precio_oferta=Decimal('18000'),
            oferta=True,
            stock=5
        )
    
    @patch('tienda.views.transaction')
    def test_creacion_pedido_exitoso(self):
        """
        Prueba 1: Creación de pedido
        
        Descripción clara de la prueba:
        Confirmar que al finalizar compra se genere un pedido correctamente con Transbank.
        
        Código involucrado:
        Vista: iniciar_pago()
        API: transaction.create()
        Variables: buy_order, session_id, amount, return_url
        """
        # Configurar el carrito en la sesión
        session = self.client.session
        session['carrito'] = {
            str(self.libro.id): {
                'titulo': self.libro.titulo,
                'precio': float(self.libro.precio),
                'cantidad': 2
            }
        }
        session.save()
        
        # Mock de respuesta de Transbank
        mock_response = {
            'url': 'https://webpay3gint.transbank.cl/webpayserver/initTransaction',
            'token': 'mock_token_abc123'
        }
        
        # Ejecución de la prueba:
        with patch('tienda.views.transaction') as mock_transaction:
            mock_transaction.create.return_value = mock_response
            
            response = self.client.post(reverse('iniciar_pago'))
            
            # Captura del resultado:
            # Verificar que se llamó a transaction.create
            mock_transaction.create.assert_called_once()
            call_args = mock_transaction.create.call_args[1]
            
            # Verificar parámetros de la llamada
            self.assertEqual(call_args['amount'], 60000)  # 2 libros x 30000
            self.assertIn('buy_order', call_args)
            self.assertIn('session_id', call_args)
            self.assertIn('return_url', call_args)
            
            # Verificar que se genera el formulario HTML
            self.assertEqual(response.status_code, 200)
            content = response.content.decode()
            self.assertIn('webpay-form', content)
            self.assertIn('mock_token_abc123', content)
            self.assertIn('webpay3gint.transbank.cl', content)
        
        # Análisis del resultado:
        print("✅ Pedido creado correctamente con Transbank, monto y datos válidos")
    
    def test_iniciar_pago_carrito_vacio(self):
        """
        Prueba adicional: Iniciar pago con carrito vacío
        
        Descripción clara de la prueba:
        Verificar que si el carrito está vacío, se redirija al carrito sin procesar el pago.
        """
        # Ejecución de la prueba (sin configurar carrito):
        response = self.client.post(reverse('iniciar_pago'))
        
        # Captura del resultado:
        # Verificar redirección al carrito
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('carrito'))
        
        # Análisis del resultado:
        print("✅ Sistema previene pago con carrito vacío correctamente")
    
    @patch('tienda.views.transaction')
    def test_pago_exitoso_pedido(self):
        """
        Prueba 2: Pago exitoso del pedido
        
        Descripción clara de la prueba:
        Comprobar que un pago realizado correctamente mediante Webpay finaliza en estado "Pagado".
        
        Código involucrado:
        Vista: pago_exito()
        API: transaction.commit()
        Verificación: response['status'] == 'AUTHORIZED'
        Template: pago_exito.html
        """
        # Mock de respuesta exitosa de Transbank
        mock_response = {
            'status': 'AUTHORIZED',
            'response_code': 0,
            'authorization_code': 'AUTH123456',
            'amount': 60000,
            'buy_order': 'order_test_123',
            'transaction_date': '2024-12-06T10:30:00Z'
        }
        
        # Ejecución de la prueba:
        with patch('tienda.views.transaction') as mock_transaction:
            mock_transaction.commit.return_value = mock_response
            
            response = self.client.post(reverse('pago_exito'), {
                'token_ws': 'token_success_test'
            })
            
            # Captura del resultado:
            # Verificar llamada correcta a commit
            mock_transaction.commit.assert_called_once_with('token_success_test')
            
            # Verificar renderizado de página de éxito
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'AUTHORIZED')
            
            # Verificar que se pasa la respuesta al template
            self.assertIn('respuesta', response.context)
            self.assertEqual(response.context['respuesta']['status'], 'AUTHORIZED')
        
        # Análisis del resultado:
        print("✅ Pago procesado exitosamente, estado AUTHORIZED confirmado")
    
    @patch('tienda.views.transaction')
    def test_pago_fallido_manejo(self):
        """
        Prueba 3: Pago fallido
        
        Descripción clara de la prueba:
        Verificar cómo el sistema gestiona un pago fallido, redirigiendo a página de error.
        
        Código involucrado:
        Vista: pago_exito()
        Condición: response['response_code'] != 0
        Redirección: redirect('pago_error')
        Template: pago_error.html
        """
        # Mock de respuesta fallida de Transbank
        mock_response = {
            'status': 'FAILED',
            'response_code': -1,
            'amount': 60000,
            'buy_order': 'order_failed_123'
        }
        
        # Ejecución de la prueba:
        with patch('tienda.views.transaction') as mock_transaction:
            mock_transaction.commit.return_value = mock_response
            
            response = self.client.post(reverse('pago_exito'), {
                'token_ws': 'token_failed_test'
            })
            
            # Captura del resultado:
            # Verificar redirección a página de error
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('pago_error'))
            
            # Verificar que la llamada a commit se realizó
            mock_transaction.commit.assert_called_once_with('token_failed_test')
        
        # Verificar que página de error es accesible
        error_response = self.client.get(reverse('pago_error'))
        self.assertEqual(error_response.status_code, 200)
        
        # Análisis del resultado:
        print("✅ Pago fallido manejado correctamente, usuario redirigido a página de error")
    
    def test_pago_sin_token(self):
        """
        Prueba adicional: Pago sin token
        
        Descripción clara de la prueba:
        Verificar que si no se proporciona token, se redirija a página de error.
        """
        # Ejecución de la prueba (sin token):
        response = self.client.post(reverse('pago_exito'))
        
        # Captura del resultado:
        # Verificar redirección a página de error
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pago_error'))
        
        # Análisis del resultado:
        print("✅ Sistema maneja correctamente la falta de token de pago")
    
    @patch('tienda.views.transaction')
    def test_excepcion_en_commit(self):
        """
        Prueba adicional: Excepción durante commit
        
        Descripción clara de la prueba:
        Verificar que si ocurre una excepción durante el commit, se redirija a página de error.
        """
        # Ejecución de la prueba:
        with patch('tienda.views.transaction') as mock_transaction:
            # Simular excepción
            mock_transaction.commit.side_effect = Exception("Error de conexión con Transbank")
            
            response = self.client.post(reverse('pago_exito'), {
                'token_ws': 'token_exception_test'
            })
            
            # Captura del resultado:
            # Verificar redirección a página de error
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('pago_error'))
        
        # Análisis del resultado:
        print("✅ Sistema maneja correctamente las excepciones durante el proceso de pago")
    
    def test_calculo_total_carrito_precios_oferta(self):
        """
        Prueba adicional: Cálculo correcto del total con precios de oferta
        
        Descripción clara de la prueba:
        Verificar que el total se calcule correctamente cuando hay libros en oferta.
        """
        # Configurar carrito con libro normal y libro en oferta
        session = self.client.session
        session['carrito'] = {
            str(self.libro.id): {
                'titulo': self.libro.titulo,
                'precio': float(self.libro.precio),  # 30000
                'cantidad': 1
            },
            str(self.libro_oferta.id): {
                'titulo': self.libro_oferta.titulo,
                'precio': float(self.libro_oferta.precio_oferta),  # 18000 (precio de oferta)
                'cantidad': 2
            }
        }
        session.save()
        
        # Mock de respuesta de Transbank
        mock_response = {
            'url': 'https://webpay3gint.transbank.cl/webpayserver/initTransaction',
            'token': 'mock_token_total_test'
        }
        
        # Ejecución de la prueba:
        with patch('tienda.views.transaction') as mock_transaction:
            mock_transaction.create.return_value = mock_response
            
            response = self.client.post(reverse('iniciar_pago'))
            
            # Captura del resultado:
            # Verificar que el total es correcto: 30000 + (18000 * 2) = 66000
            call_args = mock_transaction.create.call_args[1]
            total_esperado = 30000 + (18000 * 2)  # 66000
            self.assertEqual(call_args['amount'], total_esperado)
        
        # Análisis del resultado:
        print("✅ Cálculo del total correcto incluyendo precios de oferta")