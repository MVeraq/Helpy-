from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria

@receiver(post_migrate)
def crear_categorias_iniciales(sender, **kwargs):
    """
    Se ejecuta automáticamente después de cada 'python manage.py migrate'
    """
    # Solo ejecutar para la app Humanet
    if sender.name == 'helpy.Humanet':
        categorias = [
            {'nombre': 'Ayuda comunitaria', 'icono': '🤝', 'color': "#444D6B", 
             'descripcion': 'Mejoramiento de espacios públicos, Eventos solidarios, trueques comunitarios, etc.'},
            {'nombre': 'Asistencia alimentaria', 'icono': '🍽️', 'color': "#9CBAE0", 
             'descripcion': 'Comedores sociales, reparto de alimentos, recaudación de alimentos, etc.'},
            {'nombre': 'Salud y bienestar', 'icono': '⛑️', 'color': "#9CBAE0", 
             'descripcion': 'Campañas de vacunación, operativos medicos gratuitos, charlas de salud mental, etc.'},
            {'nombre': 'Educación y capacitación', 'icono': '📚', 'color': "#9CBAE0", 
             'descripcion': 'Talleres de oficio, Clases alfabetización'},
            {'nombre': 'Donaciones y colectas', 'icono': '❤️', 'color': "#9CBAE0", 
             'descripcion': 'Campañas de donación'},
            {'nombre': 'Ayuda a grupos vulnerables', 'icono': '👵', 'color': "#9CBAE0", 
             'descripcion': 'Apoyo a personas vulnerables'},
            {'nombre': 'Protección animal', 'icono': '🐶', 'color': "#9CBAE0", 
             'descripcion': 'Cuidado y protección animal'},
            {'nombre': 'Medio ambiente', 'icono': '🌱', 'color': "#9CBAE0", 
             'descripcion': 'Cuidado del medio ambiente'},
            {'nombre': 'Actividades recreativas', 'icono': '🎨', 'color': "#9CBAE0", 
             'descripcion': 'Actividades culturales y recreativas'},
            {'nombre': 'Trabajo en terreno', 'icono': '🥾', 'color': "#9CBAE0", 
             'descripcion': 'Limpieza espacios públicos'},
        ]
        
        for cat_data in categorias:
            Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'icono': cat_data['icono'],
                    'color': cat_data['color'],
                    'descripcion': cat_data['descripcion']
                }
            )
        
        print("✅ Categorías iniciales verificadas/creadas")