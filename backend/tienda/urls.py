from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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

    path('carrito/', views.carrito, name='carrito'),
    path('carrito.html', views.carrito, name='carrito_html'),

    path('pago/', views.iniciar_pago, name='iniciar_pago'),

    path('pago/exito/', views.pago_exito, name='pago_exito'),
    path('pago/error/', views.pago_error, name='pago_error'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)