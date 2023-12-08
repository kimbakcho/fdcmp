from django.apps import AppConfig
import sys
import os
import threading
class CapaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capa'

    def ready(self):
        if 'runserver' in sys.argv or 'fdcmp.wsgi' in sys.argv or 'fdcmp.asgi:application' in sys.argv:
            if 'runserver' in sys.argv and "--noreload" not in sys.argv:
                if not os.environ.get('RUN_MAIN'):
                    return
            from capa.Process.CapaProcessWorker import capaProcessWorker
            threading.Thread(target=capaProcessWorker,daemon=True).start()
