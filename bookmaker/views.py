from django.shortcuts import get_object_or_404, render, redirect

from .models import Bet


def index(request):
    bets = Bet.objects.all().order_by('resolve_date')
    return render(request, "bookmaker/index.html", {"bets_list": bets})


def comment_section(request, bet_id):
    bet = get_object_or_404(Bet, pk=bet_id)
    comments = bet.comments.all().order_by('-likes')
    return render(request, "bookmaker/comments.html", {"comments": comments, "bet": bet})

