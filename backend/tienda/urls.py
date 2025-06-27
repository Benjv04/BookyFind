from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import carrito_view
from django.contrib.auth import views as auth_views
from .views import cuenta_view, admin_panel, registro_usuario, login_view, admin_productos, editar_producto, admin_usuarios, eliminar_usuario, buscar_libros
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index_html'),

    path('libros/', views.libros, name='libros'),
    path('libros.html', views.libros, name='libros_html'),

    path('ofertas/', views.ofertas, name='ofertas'),
    path('ofertas.html', views.ofertas, name='ofertas_html'),

    path('contacto/', views.contacto, name='contacto'),
    path('contacto.html', views.contacto, name='contacto_html'),

    path('clubes/', views.clubes, name='clubes'),
    path('clubes.html', views.clubes, name='clubes_html'),

    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito.html', views.carrito_view, name='carrito_html'),

    path('pago/', views.iniciar_pago, name='iniciar_pago'),

    path('pago/exito/', views.pago_exito, name='pago_exito'),
    path('pago/error/', views.pago_error, name='pago_error'),

    path('libros/', views.libros, name='libros'),

    path('agregar-al-carrito/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/modificar/<str:producto_id>/<str:accion>/', views.modificar_cantidad, name='modificar_cantidad'),
    path('carrito/eliminar/<str:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path("carrito/", carrito_view, name="ver_carrito"),


    path('cuenta/', cuenta_view, name='cuenta'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('cuenta/registro/', registro_usuario, name='registro'),
    path('cuenta/login/', login_view, name='login'),
    path('admin-panel/productos/', admin_productos, name='admin_productos'),
    path('admin-panel/productos/<int:libro_id>/editar/', editar_producto, name='editar_producto'),
    path('admin-panel/usuarios/', admin_usuarios, name='admin_usuarios'),
    path('admin-panel/usuarios/<int:usuario_id>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    path('buscar/', buscar_libros, name='buscar_libros'),


]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)