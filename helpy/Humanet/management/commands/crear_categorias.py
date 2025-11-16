from django.core.management.base import BaseCommand
from Humanet.models import Categoria

class Command(BaseCommand):
    help = 'Crea las categorías predeterminadas'

    def handle(self, *args, **kwargs):
        categorias = [
        {'nombre': 'Ayuda comunitaria', 
            'icono': '🤝', 
            'color': "#444D6B", 
            'descripcion': 'Mejoramiento de espacios públicos, jornadas solidarias, ferias de trueque, apoyo barrial y organización vecinal.'},

        {'nombre': 'Asistencia alimentaria', 
            'icono': '🍽️', 
            'color': "#6A8CAF", 
            'descripcion': 'Comedores sociales, reparto de alimentos, colectas de víveres, apoyo a personas en situación de calle y bancos de alimentos.'},

        {'nombre': 'Salud y bienestar', 
            'icono': '⛑️', 
            'color': "#7EB2B2", 
            'descripcion': 'Operativos médicos gratuitos, campañas de vacunación, talleres de salud mental, controles preventivos y primeros auxilios.'},

        {'nombre': 'Educación y capacitación', 
            'icono': '📚', 
            'color': "#C49BBB", 
            'descripcion': 'Talleres de oficio, clases de alfabetización, tutorías escolares, apoyo para exámenes académicos y cursos de formación.'},

        {'nombre': 'Donaciones y colectas', 
            'icono': '❤️', 
            'color': "#E08686", 
            'descripcion': 'Recolección de ropa, campañas de útiles escolares, donación de insumos esenciales, colectas solidarias y campañas benéficas.'},

        {'nombre': 'Ayuda a grupos vulnerables', 
            'icono': '👵', 
            'color': "#B6A36A", 
            'descripcion': 'Acompañamiento a adultos mayores, apoyo a personas con discapacidad, visitas a centros de cuidado y asistencia a familias en riesgo.'},

        {'nombre': 'Protección animal', 
            'icono': '🐶', 
            'color': "#7BAF7C", 
            'descripcion': 'Rescate de animales, jornadas de adopción, esterilizaciones, alimentación de animales callejeros y cuidado veterinario.'},

        {'nombre': 'Medio ambiente', 
            'icono': '🌱', 
            'color': "#6EA96C", 
            'descripcion': 'Reforestación, reciclaje comunitario, limpieza de playas, talleres de educación ambiental y conservación de espacios naturales.'},

        {'nombre': 'Actividades recreativas', 
            'icono': '🎨', 
            'color': "#A57FB2", 
            'descripcion': 'Talleres artísticos, actividades culturales, juegos comunitarios, jornadas deportivas inclusivas y eventos de entretenimiento social.'},

        {'nombre': 'Trabajo en terreno', 
            'icono': '🥾', 
            'color': "#D4AA70", 
            'descripcion': 'Limpieza de espacios públicos, apoyo en emergencias, reparaciones básicas en hogares vulnerables y construcción comunitaria.'},

        {'nombre': 'Emergencias y desastres', 
            'icono': '🚨', 
            'color': "#DC3545", 
            'descripcion': 'Respuesta a emergencias, ayuda en desastres naturales, evacuaciones, primeros auxilios y apoyo logístico en crisis.'},

        {'nombre': 'Tecnología e innovación social', 
            'icono': '💻', 
            'color': "#4A90E2", 
            'descripcion': 'Talleres de tecnología, alfabetización digital, desarrollo de software social, hackatones solidarios y capacitación en herramientas digitales.'},

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