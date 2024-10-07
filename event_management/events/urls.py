from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('', views.lista_eventos, name='lista_eventos'),
    path('evento/crear/', views.crear_evento, name='crear_evento'),
    path('evento/<int:pk>/', views.detalle_evento, name='detalle_evento'),
    path('evento/<int:pk>/actualizar/', views.actualizar_evento, name='actualizar_evento'),
    path('evento/<int:pk>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
    path('evento/<int:pk>/registrar/', views.registrar_evento, name='registrar_evento'),
    path('mis-registros/', views.mis_registros, name='mis_registros'),
    path('registro/<int:pk>/actualizar/', views.actualizar_registro, name='actualizar_registro'),
    path('registro/<int:pk>/cancelar/', views.cancelar_registro, name='cancelar_registro'),
    path('evento/<int:pk>/usuarios-registrados/', views.usuarios_registrados_evento, name='usuarios_registrados_evento'),
    path('eventos-este-mes/', views.eventos_este_mes, name='eventos_este_mes'),
    path('usuarios-mas-activos/', views.usuarios_mas_activos, name='usuarios_mas_activos'),
    path('eventos-organizados/<int:user_id>/', views.eventos_organizados_por_usuario, name='eventos_organizados_por_usuario'),
]