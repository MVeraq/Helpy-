from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroForm, EventoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from .models import PerfilUsuario, Evento, Inscripcion, Categoria

def inicio(request):
    # Manejar el login si es un POST
    if request.method == 'POST' and 'username' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirigir a selección de preferencias si no las ha completado
            try:
                perfil = PerfilUsuario.objects.get(usuario=user)
                if not perfil.onboarding_completado:
                    return redirect('seleccionar_preferencias')
            except PerfilUsuario.DoesNotExist:
                pass
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    # Obtener eventos destacados basados en preferencias del usuario
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfilusuario
            if perfil.preferencias.exists():
                # Eventos que coinciden con las preferencias del usuario
                eventos_destacados = Evento.objects.filter(
                    categorias__in=perfil.preferencias.all()
                ).distinct().annotate(
                    coincidencias=Count('categorias', filter=Q(categorias__in=perfil.preferencias.all()))
                ).order_by('-coincidencias', '-fecha_creacion')[:6]
            else:
                eventos_destacados = Evento.objects.all().order_by('-fecha_creacion')[:6]
        except PerfilUsuario.DoesNotExist:
            eventos_destacados = Evento.objects.all().order_by('-fecha_creacion')[:6]
    else:
        eventos_destacados = Evento.objects.all().order_by('-fecha_creacion')[:6]
    
    context = {
        'eventos_destacados': eventos_destacados,
        'show_login_error': request.method == 'POST' and 'username' in request.POST
    }
    return render(request, 'Humanet/inicio.html', context)


@login_required
def seleccionar_preferencias(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    # Si ya completó el onboarding, redirigir
    if perfil.onboarding_completado:
        return redirect('inicio')
    
    if request.method == 'POST':
        categorias_ids = request.POST.getlist('categorias')
        
        if len(categorias_ids) >= 3:
            perfil.preferencias.set(categorias_ids)
            perfil.onboarding_completado = True
            perfil.save()
            messages.success(request, '¡Preferencias guardadas! Ahora verás eventos personalizados para ti.')
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor selecciona al menos 3 categorías.')
    
    categorias = Categoria.objects.all()
    return render(request, 'Humanet/seleccionar_preferencias.html', {
        'categorias': categorias
    })


def lista_eventos(request):
    eventos = Evento.objects.all()
    
    # Búsqueda por texto
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        eventos = eventos.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(ciudad__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        )
    
    # Filtro por categorías
    categorias_filtro = request.GET.getlist('categorias')
    if categorias_filtro:
        eventos = eventos.filter(categorias__id__in=categorias_filtro).distinct()
    
    # Filtro por región
    region_filtro = request.GET.get('region', '')
    if region_filtro:
        eventos = eventos.filter(region=region_filtro)
    
    # Filtro por fecha
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    if fecha_desde:
        eventos = eventos.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        eventos = eventos.filter(fecha__lte=fecha_hasta)
    
    # Ordenar por relevancia si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfilusuario
            if perfil.preferencias.exists():
                eventos = eventos.annotate(
                    coincidencias=Count('categorias', filter=Q(categorias__in=perfil.preferencias.all()))
                ).order_by('-coincidencias', '-fecha_creacion')
            else:
                eventos = eventos.order_by('-fecha_creacion')
        except PerfilUsuario.DoesNotExist:
            eventos = eventos.order_by('-fecha_creacion')
    else:
        eventos = eventos.order_by('-fecha_creacion')
    
    # Obtener todas las categorías y regiones para los filtros
    todas_categorias = Categoria.objects.all()
    regiones = Evento.REGIONES
    
    context = {
        'eventos': eventos,
        'todas_categorias': todas_categorias,
        'regiones': regiones,
        'busqueda': busqueda,
        'categorias_filtro': categorias_filtro,
        'region_filtro': region_filtro,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }
    return render(request, 'Humanet/lista_eventos.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        
        # Manejar el tipo de cuenta
        tipo_cuenta = request.POST.get('tipo_cuenta', 'individuo')
        
        if tipo_cuenta == 'organizacion':
            nombre_org = request.POST.get('nombre_organizacion', '')
            post_data = request.POST.copy()
            post_data['first_name'] = nombre_org
            post_data['last_name'] = ''
            form = RegistroForm(post_data, request.FILES)
        
        if form.is_valid():
            usuario = form.save()
            
            # Crear perfil con todos los datos adicionales
            numero_celular = request.POST.get('numero_celular', '')
            biografia = request.POST.get('biografia', '')
            foto = request.FILES.get('foto')
            
            PerfilUsuario.objects.create(
                usuario=usuario,
                tipo_cuenta=tipo_cuenta,
                numero_celular=numero_celular,
                biografia=biografia,
                foto=foto,
                onboarding_completado=False  
            )
            
            login(request, usuario)
            return redirect('seleccionar_preferencias') 
    else:
        form = RegistroForm()
    return render(request, 'Humanet/registro.html', {'form': form})



def sobre_nosotros(request):
    return render(request, 'Humanet/sobre_nosotros.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')


@login_required
def perfil(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
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
        form = EventoForm(request.POST, request.FILES)  # ← Agrega request.FILES
        if form.is_valid():
            evento = form.save(commit=False)
            evento.creador = request.user
            evento.save()
            form.save_m2m()  # Guardar las categorías (ManyToMany)
            messages.success(request, f'¡Evento "{evento.nombre}" creado exitosamente!')
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'Humanet/crear_evento.html', {'form': form})



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


@login_required
def inscribir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    # No permitir que el creador se inscriba en su propio evento
    if request.user == evento.creador:
        messages.warning(request, 'No puedes inscribirte en tu propio evento.')
        return redirect('detalle_evento', evento_id=evento_id)
    
    # Verificar si ya está inscrito
    if Inscripcion.objects.filter(evento=evento, usuario=request.user).exists():
        messages.info(request, 'Ya estás inscrito en este evento.')
        return redirect('detalle_evento', evento_id=evento_id)
    
    # Crear la inscripción
    Inscripcion.objects.create(evento=evento, usuario=request.user)
    messages.success(request, f'¡Te has inscrito exitosamente en "{evento.nombre}"!')
    return redirect('detalle_evento', evento_id=evento_id)


@login_required
def cancelar_inscripcion(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    try:
        inscripcion = Inscripcion.objects.get(evento=evento, usuario=request.user)
        inscripcion.delete()
        messages.success(request, f'Has cancelado tu inscripción en "{evento.nombre}".')
    except Inscripcion.DoesNotExist:
        messages.error(request, 'No estabas inscrito en este evento.')
    
    return redirect('detalle_evento', evento_id=evento_id)


def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscripciones = evento.inscripciones.all()
    total_inscritos = inscripciones.count()
    
    # Verificar si el usuario actual está inscrito
    usuario_inscrito = False
    if request.user.is_authenticated:
        usuario_inscrito = Inscripcion.objects.filter(evento=evento, usuario=request.user).exists()
    
    context = {
        'evento': evento,
        'inscripciones': inscripciones,
        'total_inscritos': total_inscritos,
        'usuario_inscrito': usuario_inscrito,
    }
    return render(request, 'Humanet/detalle_evento.html', context)
