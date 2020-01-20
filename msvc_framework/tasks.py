from django.conf import settings

tasks_methods = {}


def register_tasks():
    for apps in settings.INSTALLED_APPS:
        try:
            __import__(apps + '.tasks')
        except ModuleNotFoundError:
            pass
