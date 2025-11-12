from django.apps import AppConfig

class HumanetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Humanet'
    
    def ready(self):
        import Humanet.signals 