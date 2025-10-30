from django.core.management.base import BaseCommand
from Humanet.models import Categoria

class Command(BaseCommand):
    help = 'Crea las categorías predeterminadas'

    def handle(self, *args, **kwargs):
        categorias = [
            {'nombre': 'Ayuda comunitaria', 'icono': '🤝', 'color':"#444D6B", 'descripcion': 'Mejoramiento de espacios públicos, Eventos solidarios, trueques comunitarios, etc.'},
            {'nombre': 'Asistencia alimentaria', 'icono': '🍽️', 'color':"#9CBAE0", 'descripcion': 'Comedores sociales, reparto de alimentos, recaudación de alimentos, etc.'},
            {'nombre': 'Salud y bienestar', 'icono': '⛑️', 'color':"#9CBAE0", 'descripcion': 'Campañas de vacunación, operativos medicos gratuitos, charlas de salud mental, etc. '},
            {'nombre': 'Educación y capacitación', 'icono': '📚', 'color':"#9CBAE0", 'descripcion': 'Talleres de oficio, Clases alfabetización, '},
            {'nombre': 'Donaciones y colectas', 'icono': '❤️', 'color':"#9CBAE0", 'descripcion': ''},
            {'nombre': 'Ayuda a grupos vulnerables', 'icono': '👵', 'color':"#9CBAE0", 'descripcion': ''},
            {'nombre': 'Protección animal', 'icono': '🐶', 'color':"#9CBAE0", 'descripcion': ''},
            {'nombre': 'Medio ambiente', 'icono': '🌱', 'color':"#9CBAE0", 'descripcion': ''},
            {'nombre': 'Actividades recreativas', 'icono': '🎨', 'color':"#9CBAE0", 'descripcion': ''},
            {'nombre': 'Trabajo en terreno', 'icono': '🥾', 'color':"#9CBAE0", 'descripcion': 'Limpieza espacios públicos, '},
        ]
            
        
        for cat_data in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'icono': cat_data['icono'],
                    'color': cat_data['color'],
                    'descripcion': cat_data['descripcion']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Creada: {categoria}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  Ya existe: {categoria}'))