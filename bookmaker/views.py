from django.shortcuts import get_object_or_404, render, redirect

from .models import Bet, UserProfile


def index(request):
    bets = Bet.objects.all().order_by('resolve_date')
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user.id)
    return render(request, "bookmaker/index.html", {"bets_list": bets, "user_profile": user_profile})


def comment_section(request, bet_id):
    bet = get_object_or_404(Bet, pk=bet_id)
    comments = bet.comments.all().order_by('-likes')
    return render(request, "bookmaker/comments.html", {"comments": comments, "bet": bet})

