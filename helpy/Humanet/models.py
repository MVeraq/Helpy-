from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    icono = models.CharField(max_length=10, default='📌')  
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#667eea')  
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.icono} {self.nombre}"


class PerfilUsuario(models.Model):
    TIPO_CUENTA = [
        ('individuo', 'Individuo'),
        ('organizacion', 'Organización'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA, default='individuo')
    numero_celular = models.CharField(max_length=15, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    # NUEVO: Preferencias de categorías
    preferencias = models.ManyToManyField(Categoria, blank=True, related_name='usuarios_interesados')
    onboarding_completado = models.BooleanField(default=False)  # Para saber si eligió preferencias

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Evento(models.Model):
    REGIONES = [
        ('tarapaca', 'Tarapacá'),
        ('antofagasta', 'Antofagasta'),
        ('atacama', 'Atacama'),
        ('coquimbo', 'Coquimbo'),
        ('valparaiso', 'Valparaíso'),
        ('ohiggins', "O'Higgins"),
        ('maule', 'Maule'),
        ('nuble', 'Ñuble'),
        ('biobio', 'Biobío'),
        ('araucania', 'La Araucanía'),
        ('los_rios', 'Los Ríos'),
        ('los_lagos', 'Los Lagos'),
        ('aysen', 'Aysén'),
        ('magallanes', 'Magallanes'),
        ('metropolitana', 'Metropolitana'),
        ('arica', 'Arica y Parinacota'),
    ]
    
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos')
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)  # NUEVO
    fecha = models.DateField()
    hora = models.TimeField()
    
    # Ubicación detallada
    ubicacion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100, blank=True, null=True)  # NUEVO
    region = models.CharField(max_length=50, choices=REGIONES, blank=True, null=True)  # NUEVO
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    descripcion = models.TextField()
    detalles = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    categorias = models.ManyToManyField(Categoria, related_name='eventos')
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha}"

class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscripciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('evento', 'usuario')
        ordering = ['-fecha_inscripcion']
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
    
    def __str__(self):
        return f"{self.usuario.username} → {self.evento.nombre}"