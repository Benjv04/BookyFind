from django.shortcuts import render

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
