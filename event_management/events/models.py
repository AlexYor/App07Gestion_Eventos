from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('El campo Username es obligatorio')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
        ('cancelado', 'Cancelado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    capacidad_maxima = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    organizador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_organizados')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='eventos')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class RegistroEvento(models.Model):
    ESTADO_REGISTRO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='registros')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_registrados')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_REGISTRO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True)

    class Meta:
        unique_together = ('evento', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.titulo}"

class Comentario(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.evento.titulo}"