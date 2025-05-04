from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import carrito_view

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

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)