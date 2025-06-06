from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Libro  # tu modelo personalizado

class UsuarioCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducciones personalizadas
        self.fields['username'].label = "Nombre de usuario"
        self.fields['username'].help_text = "Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_"
        self.fields['password1'].label = "Contraseña"
        self.fields['password1'].help_text = "Debe tener al menos 8 caracteres y no ser solo numérica."
        self.fields['password2'].label = "Confirmar contraseña"
        self.fields['password2'].help_text = "Ingresa la misma contraseña para verificarla."

    class Meta:
        model = Usuario
        fields = ('username', 'email')  # ajusta según tus campos



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'descripcion', 'precio', 'precio_oferta', 'oferta', 'stock', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }