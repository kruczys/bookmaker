from celery import Celery


def make_celery(app_name):
    backend = 'pyamqp://guest@localhost//'
    broker = 'pyamqp://guest@localhost//'
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery('main')
