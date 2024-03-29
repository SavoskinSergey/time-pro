from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.employee'
    label = 'core_employee'

    def ready(self):
        import core.employee.signals
