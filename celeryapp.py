from celery import Celery


def make_celery(app_name):
    backend = 'redis://localhost:6379/0'
    broker = 'redis://localhost:6379/0'
    return Celery(app_name, backend=backend, broker=broker)


celery = make_celery('main')

# sudo systemctl enable mosquitto
# sudo systemctl start mosquitto
# redis-server
# celery -A main.celery worker --loglevel=info
# celery -A main.celery beat --loglevel=info