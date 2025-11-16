from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.inicio, name='inicio'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('registro/', views.registro, name='registro'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='Humanet/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Preferencias y perfil
    path('preferencias/', views.seleccionar_preferencias, name='seleccionar_preferencias'),
    path('perfil/', views.perfil, name='perfil'),
    path('usuario/<str:username>/', views.perfil_publico, name='perfil_publico'),
    
    # Eventos
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:evento_id>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
    path('eventos/<int:evento_id>/inscribir/', views.inscribir_evento, name='inscribir_evento'),
    path('eventos/<int:evento_id>/cancelar/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
]