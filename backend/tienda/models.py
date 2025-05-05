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
    editorial = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='libros/', blank=True, null=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo

class Pedido(models.Model):
    ESTADOS = (
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('failed', 'Fallido'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    libros = models.ManyToManyField(Libro)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pending')

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username} - {self.fecha.strftime("%d/%m/%Y")}'

class Pago(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    estado = models.CharField(max_length=20)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, default='Webpay Plus')

    def __str__(self):
        return f"Pago {self.pedido.id} - {self.estado}"