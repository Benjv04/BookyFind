from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Libro, Pedido

class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('rol', 'nombre', 'email', 'telefono', 'direccion')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'nombre', 'rol', 'telefono', 'direccion')
        }),
    )
    list_display = ('username', 'email', 'nombre', 'rol', 'telefono')
    search_fields = ('email', 'nombre', 'username')
    ordering = ('email',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Libro)
admin.site.register(Pedido)