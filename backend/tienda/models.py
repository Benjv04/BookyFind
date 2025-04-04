from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
    )
    
    rol = models.CharField(max_length=10, choices=ROLES, default='cliente')
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_rol_display()})"

class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    libros = models.ManyToManyField(Libro)

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username} - {self.fecha.strftime("%d/%m/%Y")}'
    
