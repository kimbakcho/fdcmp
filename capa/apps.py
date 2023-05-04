from django.apps import AppConfig
import sys
import os
class CapaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capa'

    def ready(self):
        if 'runserver' in sys.argv or 'fdcmp.wsgi' in sys.argv or 'fdcmp.asgi:application' in sys.argv:
            if 'runserver' in sys.argv:
                if not os.environ.get('RUN_MAIN'):
                    return
