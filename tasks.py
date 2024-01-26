from celeryapp import celery
from cruds import BetManager, client


@celery.task
def resolve_bets():
    bet_manager = BetManager(client)
    bet_manager.resolve_bets()


celery.conf.beat_schedule = {
    'resolve-bets-every-minute': {
        'task': 'tasks.resolve_bets',
        'schedule': 60.0
    },
}
