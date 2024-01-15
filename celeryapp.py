from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmakerProject.settings')
app = Celery('bookmakerProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'resolve-bets-every-minute': {
        'task': 'bookmaker.tasks.resolve_bets',
        'schedule': 60,
    },
}

if __name__ == '__main__':
    app.start()

# celery -A celeryapp worker --loglevel=info
# celery -A celeryapp beat --loglevel=info