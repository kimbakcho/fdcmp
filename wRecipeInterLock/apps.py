import logging
import os
import sys

from django.apps import AppConfig


class WrecipeinterlockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wRecipeInterLock'

    def ready(self):
        if 'runserver' in sys.argv or 'fdcmp.wsgi' in sys.argv or 'fdcmp.asgi:application' in sys.argv:
            if 'runserver' in sys.argv and "--noreload" not in sys.argv:
                if not os.environ.get('RUN_MAIN'):
                    return
            logging.getLogger("wRIL").info("startService")

            from wRecipeInterLock.Process.WRILProcessWorker import wrilProcessWorker
            wrilProcessWorker()