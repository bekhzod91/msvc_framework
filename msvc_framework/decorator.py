from .tasks import tasks_methods


def tasks(path):
    def wrapper(func):
        data = {
            'func': func,
            'path': path
        }

        tasks_methods[path] = data

    return wrapper

