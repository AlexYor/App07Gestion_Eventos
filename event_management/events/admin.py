from django.contrib import admin
from .models import  Usuario, Categoria, Evento, RegistroEvento, Comentario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Evento)
admin.site.register(RegistroEvento)
admin.site.register(Comentario)