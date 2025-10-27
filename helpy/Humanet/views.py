from django.shortcuts import render, redirect
from .forms import RegistroForm, EventoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import PerfilUsuario, Evento, User
from django.shortcuts import get_object_or_404
from django.contrib import messages

def inicio(request):
    # Obtener los últimos 3 eventos para mostrar en la página de inicio
    eventos_destacados = Evento.objects.all().order_by('-fecha')[:3]
    return render(request, 'Humanet/inicio.html', {'eventos_destacados': eventos_destacados})

def sobre_nosotros(request):
    return render(request, 'Humanet/sobre_nosotros.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()

            
            tipo_cuenta = form.cleaned_data.get('tipo_cuenta')
            numero_celular = form.cleaned_data.get('numero_celular')
            biografia = form.cleaned_data.get('biografia')
            foto = form.cleaned_data.get('foto')


            PerfilUsuario.objects.create(usuario=usuario, tipo_cuenta=tipo_cuenta, numero_celular=numero_celular, biografia=biografia, foto=foto) 
            login(request, usuario)

            tipo_cuenta = form.cleaned_data.get('tipo_cuenta')

            return redirect('login')
            
    else:
        form = RegistroForm()
    return render(request, 'Humanet/registro.html', {'form': form})


@login_required
def perfil(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    # Verificar si hay mensaje en la URL
    mensaje = request.GET.get('mensaje')
    evento_nombre = request.GET.get('evento', '')
    
    context = {
        'perfil': perfil,
        'mensaje': mensaje,
        'evento_nombre': evento_nombre
    }
    
    return render(request, 'Humanet/perfil.html', context)


@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.creador = request.user
            evento.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'Humanet/crear_evento.html', {'form': form})



def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'Humanet/lista_eventos.html', {'eventos': eventos})



def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'Humanet/detalle_evento.html', {'evento': evento})


def perfil_publico(request, username):
    usuario = get_object_or_404(User, username=username)
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=usuario)
    eventos_creados = Evento.objects.filter(creador=usuario)
   


    context = {
        'usuario_perfil': usuario,
        'perfil': perfil,
        'eventos_creados': eventos_creados,
    }
    return render(request, 'Humanet/perfil_publico.html', context)

@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar que el usuario sea el creador O sea administrador
    if request.user == evento.creador or request.user.is_staff:
        if request.method == 'POST':
            # Verificar la contraseña antes de eliminar
            password = request.POST.get('password')
            user = authenticate(username=request.user.username, password=password)
            
            if user is not None:
                # Contraseña correcta - proceder a eliminar
                nombre_evento = evento.nombre
                evento.delete()
                print(f"Evento {nombre_evento} eliminado exitosamente")
                # Redirigir al perfil con mensaje de éxito
                return redirect('perfil')
            else:
                # Contraseña incorrecta
                messages.error(request, '❌ Contraseña incorrecta. El evento no fue eliminado.')
                return render(request, 'Humanet/confirmar_eliminar.html', {'evento': evento})
        else:
            # Mostrar página de confirmación
            return render(request, 'Humanet/confirmar_eliminar.html', {'evento': evento})
    else:
        messages.error(request, 'No tienes permiso para eliminar este evento.')
        return redirect('detalle_evento', evento_id=evento_id)
