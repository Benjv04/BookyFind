from django.db import models

# Create your models here.
class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    libros = models.ManyToManyField(Libro)
    
    def __str__(self):
        return f'Pedido {self.id} - {self.fecha.strftime("%d/%m/%Y")}'
