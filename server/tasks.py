from server.celeryapp import celery
from server.bet_manager import BetManager
from server.main import mqtt_client


@celery.task
def resolve_bets():
    bet_manager = BetManager(mqtt_client)
    bet_manager.resolve_bets()


celery.conf.beat_schedule = {
    'resolve-bets-every-minute': {
        'task': 'tasks.resolve_bets',
        'schedule': 60.0
    },
}
