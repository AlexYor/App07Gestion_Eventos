from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Evento, RegistroEvento, Usuario, Comentario
from .forms import EventoForm, RegistroEventoForm, ComentarioForm, UsuarioCreationForm, UsuarioLoginForm

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

def registro_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido!')
            return redirect('lista_eventos')
    else:
        form = UsuarioCreationForm()
    return render(request, 'events/registro_usuario.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = UsuarioLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Has iniciado sesión como {username}.")
                return redirect('lista_eventos')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    form = UsuarioLoginForm()
    return render(request, 'events/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect(reverse('login'))

@login_required
def lista_eventos(request):
    eventos = Evento.objects.filter(estado='publicado').order_by('fecha_inicio')
    paginator = Paginator(eventos, 10)  # Mostrar 10 eventos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/lista_eventos.html', {'page_obj': page_obj})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.save()
            messages.success(request, 'Evento creado exitosamente.')
            return redirect('detalle_evento', pk=evento.pk)
    else:
        form = EventoForm()
    return render(request, 'events/crear_evento.html', {'form': form})

@login_required
def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.evento = evento
            comentario.usuario = request.user
            comentario.save()
            messages.success(request, 'Comentario añadido exitosamente.')
            return redirect('detalle_evento', pk=pk)
    else:
        form = ComentarioForm()
    return render(request, 'events/detalle_evento.html', {'evento': evento, 'form': form})

@login_required
def actualizar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.user != evento.organizador:
        messages.error(request, 'No tienes permiso para actualizar este evento.')
        return redirect('detalle_evento', pk=pk)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado exitosamente.')
            return redirect('detalle_evento', pk=pk)
    else:
        form = EventoForm(instance=evento)
    return render(request, 'events/actualizar_evento.html', {'form': form, 'evento': evento})

@login_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.user != evento.organizador:
        messages.error(request, 'No tienes permiso para eliminar este evento.')
        return redirect('detalle_evento', pk=pk)
    
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado exitosamente.')
        return redirect('lista_eventos')
    return render(request, 'events/eliminar_evento.html', {'evento': evento})

@login_required
def registrar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.evento = evento
            registro.usuario = request.user
            registro.save()
            messages.success(request, 'Te has registrado exitosamente en el evento.')
            return redirect('detalle_evento', pk=pk)
    else:
        form = RegistroEventoForm()
    return render(request, 'events/registrar_evento.html', {'form': form, 'evento': evento})

@login_required
def mis_registros(request):
    registros = RegistroEvento.objects.filter(usuario=request.user)
    return render(request, 'events/mis_registros.html', {'registros': registros})

@login_required
def actualizar_registro(request, pk):
    registro = get_object_or_404(RegistroEvento, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro actualizado exitosamente.')
            return redirect('mis_registros')
    else:
        form = RegistroEventoForm(instance=registro)
    return render(request, 'events/actualizar_registro.html', {'form': form, 'registro': registro})

@login_required
def cancelar_registro(request, pk):
    registro = get_object_or_404(RegistroEvento, pk=pk, usuario=request.user)
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro cancelado exitosamente.')
        return redirect('mis_registros')
    return render(request, 'events/cancelar_registro.html', {'registro': registro})

@login_required
def usuarios_registrados_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    cantidad_usuarios = evento.registros.count()
    return render(request, 'events/usuarios_registrados_evento.html', {'evento': evento, 'cantidad_usuarios': cantidad_usuarios})

@login_required
def eventos_este_mes(request):
    hoy = timezone.now()
    primer_dia_mes = hoy.replace(day=1)
    ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    eventos = Evento.objects.filter(fecha_inicio__range=(primer_dia_mes, ultimo_dia_mes))
    cantidad_eventos = eventos.count()
    return render(request, 'events/eventos_este_mes.html', {'eventos': eventos, 'cantidad_eventos': cantidad_eventos})

@login_required
def usuarios_mas_activos(request):
    usuarios_activos = Usuario.objects.annotate(num_registros=Count('eventos_registrados')).order_by('-num_registros')[:10]
    return render(request, 'events/usuarios_mas_activos.html', {'usuarios_activos': usuarios_activos})

@login_required
def eventos_organizados_por_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    eventos = Evento.objects.filter(organizador=usuario)
    cantidad_eventos = eventos.count()
    return render(request, 'events/eventos_organizados_por_usuario.html', {'usuario': usuario, 'eventos': eventos, 'cantidad_eventos': cantidad_eventos})