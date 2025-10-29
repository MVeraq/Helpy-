from django.core.management.base import BaseCommand
from Humanet.models import Categoria

class Command(BaseCommand):
    help = 'Crea las categorías predeterminadas'

    def handle(self, *args, **kwargs):
        categorias = [
            {'nombre': '', 'icono': '', 'color': , 'descripcion': ''},
        
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