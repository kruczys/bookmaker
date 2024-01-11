from django.shortcuts import get_object_or_404, render

from bookmaker.models import Bet


def index(request):
    bets = Bet.objects.all()
    return render(request, "bookmaker/index.html", {"bets_list": bets})


def comment_section(request, bet_id):
    bet = get_object_or_404(Bet, pk=bet_id)
    comments = bet.comments.all()
    return render(request, "bookmaker/comments.html", {"comments": comments, "bet": bet})
