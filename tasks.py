from celeryapp import celery
from main import BetManager, users, user_bets, bets


@celery.task
def resolve_bets():
    bet_manager = BetManager(users=users, user_bets=user_bets, bets=bets)
    bet_manager.resolve_bets()


celery.conf.beat_schedule = {
    'resolve-bets-every-minute': {
        'task': 'tasks.resolve_bets',
        'schedule': 60.0
    },
}
