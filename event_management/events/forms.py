from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Evento, RegistroEvento, Comentario

class UsuarioCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=15, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    fecha_nacimiento = forms.DateField(required=False)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'telefono', 'bio', 'fecha_nacimiento')

class UsuarioLoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'ubicacion', 'capacidad_maxima', 'precio', 'categoria', 'imagen']

class RegistroEventoForm(forms.ModelForm):
    class Meta:
        model = RegistroEvento
        fields = ['notas']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']