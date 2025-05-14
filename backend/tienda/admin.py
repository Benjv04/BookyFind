from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Libro, Pedido

class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'nombre', 'telefono', 'direccion')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'nombre', 'rol', 'telefono', 'direccion'),
        }),
    )
    list_display = ('username', 'email', 'nombre', 'rol', 'telefono')
    search_fields = ('email', 'nombre', 'username')
    ordering = ('email',)

class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'precio', 'oferta', 'precio_oferta')
    list_filter = ('oferta', 'editorial')
    search_fields = ('titulo', 'autor')
    fields = ('titulo', 'autor', 'editorial', 'precio', 'stock', 'descripcion', 'imagen',
              'fecha_publicacion', 'oferta', 'precio_oferta')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Libro)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Pedido)
