from django.urls import path
from . import views  

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.libros, name='libros'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('contacto/', views.contacto, name='contacto'),
    path('clubes/', views.clubes, name='clubes'),
    path('carrito/', views.carrito, name='carrito'),
]