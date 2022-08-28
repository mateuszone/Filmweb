from django.apps import AppConfig
from django.conf import settings

class basicConfig(AppConfig):
    name = 'basic'
    app_label = 'basic'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import basic.signals
