from random import randint

from celery import shared_task

from .models import Bet


@shared_task
def resolve_bets():
    bets = Bet.objects.all()
    for bet in bets:
        if bet.is_resolved() and not bet.resolved:
            bet.result = randint(0, 2)
            bet.resolved = True
            bet.save()
