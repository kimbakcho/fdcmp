import sys

from django.apps import AppConfig


class McpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mcp'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
