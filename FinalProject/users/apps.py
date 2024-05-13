from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    #Connect signals.py file to the app
    def ready(self):
        import users.signals
