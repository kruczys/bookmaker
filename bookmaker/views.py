from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from bookmaker.models import Comment, Bet


class IndexListView(ListView):
    queryset = Bet.objects.order_by('resolve_date')
    model = Bet
    template_name = 'bookmaker/index.html'
    context_object_name = "bets_list"


def comment_section(request, bet_id):
    bet = get_object_or_404(Bet, pk=bet_id)
    comments = bet.comments.all()
    return render(request, "bookmaker/comments.html", {"comments": comments, "bet": bet})
