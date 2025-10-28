from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    TIPO_CUENTA = [
        ('individuo', 'Individuo'),
        ('organizacion', 'Organización'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_celular = models.CharField(max_length=15, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA, default='individuo')

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    

class Evento(models.Model):
    
    
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos')
    nombre = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    ubicacion = models.CharField(max_length=300)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    descripcion = models.TextField()
    detalles = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
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
        unique_together = ('evento', 'usuario')  # Un usuario no puede inscribirse dos veces al mismo evento
        ordering = ['-fecha_inscripcion']
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
    
    def __str__(self):
        return f"{self.usuario.username} → {self.evento.nombre}"
