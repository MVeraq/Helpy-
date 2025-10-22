from django.shortcuts import render, redirect
from .forms import RegistroForm, EventoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import PerfilUsuario, Evento
from django.shortcuts import get_object_or_404

def inicio(request):
    return render(request, 'Humanet/inicio.html')

def sobre_nosotros(request):
    return render(request, 'Humanet/sobre_nosotros.html')

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
    return render(request, 'Humanet/perfil.' \
    'html', {'perfil': perfil})


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
    return render(request, 'Humanet/detalle_evento.html', {'evento': evento})@login_required


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
