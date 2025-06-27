from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from unittest.mock import patch
from decimal import Decimal
from .models import Libro
from django.core.files.base import ContentFile
from io import BytesIO

User = get_user_model()

class GestionUsuariosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario_existente = User.objects.create_user(
            username='benj.gonzalezn@duocuc.cl',
            email='benj.gonzalezn@duocuc.cl',
            password='Contraseña123'
        )

    def test_creacion_usuario_datos_validos(self):
        datos = {
            'username': 'ejemplo1@duocuc.cl',
            'email': 'ejemplo1@duocuc.cl',
            'password1': 'Contraseña123',
            'password2': 'Contraseña123'
        }
        response = self.client.post(reverse('registro'), datos)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='ejemplo1@duocuc.cl').exists())
        mensajes = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any("cuenta ha sido creada correctamente" in str(m) for m in mensajes))
        print("Usuario creado correctamente")

    def test_login_credenciales_incorrectas(self):
        datos = {
            'username': 'benj.gonzalezn@duocuc.cl',
            'password': 'ContraseñaIncorrecta123'
        }
        response = self.client.post(reverse('login'), datos)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        mensajes = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any("Credenciales invalidas" in str(m) for m in mensajes))
        print("Login fallido correctamente")

    def test_registro_email_duplicado(self):
        datos = {
            'username': 'benj.gonzalezn@duocuc.cl',
            'email': 'benj.gonzalezn@duocuc.cl',
            'password1': 'Contraseña123',
            'password2': 'Contraseña123'
        }
        response = self.client.post(reverse('registro'), datos)
        self.assertEqual(response.status_code, 200)
        count = User.objects.filter(username='benj.gonzalezn@duocuc.cl').count()
        self.assertEqual(count, 1)
        self.assertContains(response, 'error')
        print("Registro con email repetido bloqueado")


class CatalogoLibrosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        image_file = BytesIO(b"fake image content")
        image_file.name = 'test_image.jpg'
        self.libro1 = Libro.objects.create(
            titulo="El Quijote",
            autor="Miguel de Cervantes",
            editorial="Editorial Planeta",
            descripcion="Novela clasica",
            precio=Decimal('15000'),
            stock=10,
            oferta=False,
            imagen=ContentFile(image_file.read(), name='test_image.jpg')
        )
        self.libro2 = Libro.objects.create(
            titulo="Cien años de soledad",
            autor="Gabriel Garcia Marquez",
            editorial="Editorial Sudamericana",
            descripcion="Realismo magico",
            precio=Decimal('20000'),
            precio_oferta=Decimal('15000'),
            stock=5,
            oferta=True,
            imagen=ContentFile(image_file.read(), name='test_image.jpg')
        )
        self.libro3 = Libro.objects.create(
            titulo="1984",
            autor="George Orwell",
            editorial="Editorial Planeta",
            descripcion="Distopia clasica",
            precio=Decimal('18000'),
            stock=8,
            imagen=ContentFile(image_file.read(), name='test_image.jpg')
        )

    def test_visualizacion_libros_disponibles(self):
        response = self.client.get(reverse('libros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El Quijote")
        self.assertContains(response, "Cien años de soledad")
        self.assertContains(response, "1984")
        self.assertContains(response, "$15000")
        self.assertContains(response, "$18000")
        self.assertContains(response, "Agregar al carrito", count=6)
        print("Libros mostrados correctamente")

    def test_visualizar_detalle_libros_modal(self):
        response = self.client.get(reverse('libros'))
        content = response.content.decode()
        self.assertIn(f'modalLibro{self.libro1.id}', content)
        self.assertIn(f'modalLibro{self.libro2.id}', content)
        self.assertContains(response, "Miguel de Cervantes")
        self.assertContains(response, "Editorial Planeta")
        self.assertContains(response, "Gabriel Garcia Marquez")
        self.assertContains(response, "Novela clasica")
        print("Detalle de libros visible en modal")

    def test_libros_con_oferta_precio_correcto(self):
        response = self.client.get(reverse('libros'))
        content = response.content.decode()
        self.assertIn('<del>$20000</del>', content)
        self.assertIn('$15000', content)
        self.assertIn('oferta_png.png', content)
        self.assertNotIn('<del>$15000</del>', content)
        print("Precios de oferta mostrados correctamente")


class CarritoComprasTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.libro = Libro.objects.create(
            titulo="Libro Test",
            autor="Autor Test",
            precio=Decimal('12000'),
            stock=10
        )
        self.libro_oferta = Libro.objects.create(
            titulo="Libro Oferta",
            autor="Autor Test",
            precio=Decimal('25000'),
            precio_oferta=Decimal('18000'),
            oferta=True,
            stock=5
        )

    def test_agregar_libro_al_carrito(self):
        response = self.client.post(reverse('agregar_al_carrito', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        carrito = self.client.session.get('carrito', {})
        self.assertIn(str(self.libro.id), carrito)
        item = carrito[str(self.libro.id)]
        self.assertEqual(item['titulo'], "Libro Test")
        self.assertEqual(item['precio'], 12000.0)
        self.assertEqual(item['cantidad'], 1)
        print("Libro agregado al carrito")

    def test_eliminar_libro_del_carrito(self):
        self.client.post(reverse('agregar_al_carrito', args=[self.libro.id]))
        response = self.client.post(reverse('eliminar_del_carrito', args=[self.libro.id]))
        self.assertEqual(response.status_code, 302)
        carrito = self.client.session.get('carrito', {})
        self.assertNotIn(str(self.libro.id), carrito)
        print("Libro eliminado del carrito")

    def test_modificar_cantidad_en_carrito(self):
        self.client.post(reverse('agregar_al_carrito', args=[self.libro.id]))
        self.client.post(reverse('modificar_cantidad', args=[self.libro.id, 'sumar']))
        carrito = self.client.session.get('carrito', {})
        self.assertEqual(carrito[str(self.libro.id)]['cantidad'], 2)
        self.client.post(reverse('modificar_cantidad', args=[self.libro.id, 'restar']))
        carrito = self.client.session.get('carrito', {})
        self.assertEqual(carrito[str(self.libro.id)]['cantidad'], 1)
        print("Cantidad modificada correctamente")


class PedidosPagosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.libro = Libro.objects.create(
            titulo="Libro Pago",
            autor="Autor Pago",
            editorial="Edit",
            descripcion="Descripcion",
            precio=Decimal('30000'),
            stock=10
        )
        self.libro_oferta = Libro.objects.create(
            titulo="Libro Oferta Pago",
            autor="Autor Pago",
            editorial="Edit",
            descripcion="Oferta",
            precio=Decimal('25000'),
            precio_oferta=Decimal('18000'),
            oferta=True,
            stock=5
        )

    @patch('tienda.views.transaction')
    def test_creacion_pedido_exitoso(self, mock_transaction):
        session = self.client.session
        session['carrito'] = {
            str(self.libro.id): {
                'titulo': self.libro.titulo,
                'precio': float(self.libro.precio),
                'cantidad': 2
            }
        }
        session.save()
        mock_transaction.create.return_value = {
            'url': 'https://webpay3gint.transbank.cl',
            'token': 'mock_token'
        }
        response = self.client.post(reverse('iniciar_pago'))
        args = mock_transaction.create.call_args[1]
        self.assertEqual(args['amount'], 60000)
        self.assertIn('mock_token', response.content.decode())
        print("Pedido creado correctamente")

    def test_iniciar_pago_carrito_vacio(self):
        response = self.client.post(reverse('iniciar_pago'))
        self.assertRedirects(response, reverse('carrito'))
        print("No se puede pagar con carrito vacio")

    @patch('tienda.views.transaction')
    def test_pago_exitoso_pedido(self, mock_transaction):
        mock_transaction.commit.return_value = {
            'status': 'AUTHORIZED',
            'response_code': 0,
            'authorization_code': 'AUTH123',
            'amount': 60000,
            'buy_order': 'test_order'
        }
        response = self.client.post(reverse('pago_exito'), {
            'token_ws': 'token_test'
        })
        self.assertContains(response, 'AUTHORIZED')
        print("Pago exitoso confirmado")

    @patch('tienda.views.transaction')
    def test_pago_fallido_manejo(self, mock_transaction):
        mock_transaction.commit.return_value = {
            'status': 'FAILED',
            'response_code': -1
        }
        response = self.client.post(reverse('pago_exito'), {
            'token_ws': 'token_fail'
        })
        self.assertRedirects(response, reverse('pago_error'))
        print("Pago fallido manejado correctamente")

    def test_pago_sin_token(self):
        response = self.client.post(reverse('pago_exito'))
        self.assertRedirects(response, reverse('pago_error'))
        print("Pago sin token redirigido")

    @patch('tienda.views.transaction')
    def test_excepcion_en_commit(self, mock_transaction):
        mock_transaction.commit.side_effect = Exception("Error")
        response = self.client.post(reverse('pago_exito'), {
            'token_ws': 'token'
        })
        self.assertRedirects(response, reverse('pago_error'))
        print("Excepcion manejada correctamente")

    @patch('tienda.views.transaction')
    def test_calculo_total_carrito_precios_oferta(self, mock_transaction):
        session = self.client.session
        session['carrito'] = {
            str(self.libro.id): {
                'titulo': self.libro.titulo,
                'precio': float(self.libro.precio),
                'cantidad': 1
            },
            str(self.libro_oferta.id): {
                'titulo': self.libro_oferta.titulo,
                'precio': float(self.libro_oferta.precio_oferta),
                'cantidad': 2
            }
        }
        session.save()
        mock_transaction.create.return_value = {
            'url': 'https://webpay3gint.transbank.cl',
            'token': 'token'
        }
        self.client.post(reverse('iniciar_pago'))
        args = mock_transaction.create.call_args[1]
        self.assertEqual(args['amount'], 66000)
        print("Total del carrito calculado correctamente")
