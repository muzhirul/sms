from django.apps import AppConfig
from django.conf import settings


class StaffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from sms import operators
            operators.data_update_start()
