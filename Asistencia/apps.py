from django.apps import AppConfig


class AsistenciaConfig(AppConfig):
    name = 'Asistencia'
    
    def ready(self):
        from . import signals
