from django.contrib import admin
from Humanet.models import Categoria, PerfilUsuario, Evento, Inscripcion


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono', 'color', 'descripcion_corta')
    list_filter = ('nombre',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    
    def descripcion_corta(self, obj):
        """Muestra una versión corta de la descripción"""
        if obj.descripcion:
            return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
        return '-'
    descripcion_corta.short_description = 'Descripción'


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_cuenta', 'numero_celular', 'onboarding_completado')
    list_filter = ('tipo_cuenta', 'onboarding_completado')
    search_fields = ('usuario__username', 'usuario__email', 'numero_celular')
    filter_horizontal = ('preferencias',)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'creador', 'fecha', 'hora', 'ciudad', 'region')
    list_filter = ('fecha', 'region', 'categorias')
    search_fields = ('nombre', 'descripcion', 'creador__username', 'ciudad')
    filter_horizontal = ('categorias',)
    date_hierarchy = 'fecha'
    readonly_fields = ('fecha_creacion',)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_inscripcion')
    list_filter = ('fecha_inscripcion',)
    search_fields = ('usuario__username', 'evento__nombre')
    date_hierarchy = 'fecha_inscripcion'
    readonly_fields = ('fecha_inscripcion',)

