from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone

from .forms import CreateBetForm, UserBetForm, CreateCommentForm
from .models import Bet, UserProfile, UserBet


def index(request):
    bets = Bet.objects.all().order_by('-resolve_date')
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user.id)
    return render(request, "bookmaker/index.html", {"bets_list": bets, "user_profile": user_profile})


def user_info(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_bets = UserBet.objects.filter(user=user_profile)
    return render(request, "bookmaker/info.html", {
        "user_profile": user_profile,
        "user_bets": user_bets,
    })


def comment_section(request, bet_id):
    bet = get_object_or_404(Bet, pk=bet_id)
    comments = bet.comments.all().order_by('-likes')
    return render(request, "bookmaker/comments.html", {"comments": comments, "bet": bet})


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('bookmaker:index')
    template_name = "registration/signup.html"


def create_bet(request):
    if request.method == 'POST':
        form = CreateBetForm(request.POST)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.save()
            return redirect('bookmaker:index')
    else:
        form = CreateBetForm()
    return render(request, 'bookmaker/create_bet.html', {'form': form})


def create_comment(request, bet_id):
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.bet = Bet.objects.get(id=bet_id)
            comment.user = UserProfile.objects.get(user=request.user)
            comment.pub_date = timezone.now()
            comment.save()
            return redirect('bookmaker:comments', bet_id=comment.bet.id)
    else:
        form = CreateCommentForm()
    return render(request, 'bookmaker/create_comment.html', {'form': form})


def place_bet(request, bet_id):
    bet = get_object_or_404(Bet, pk=bet_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserBetForm(request.POST)
        if form.is_valid():
            user_bet = form.save(commit=False)
            user_bet.user = user_profile
            user_bet.bet = bet
            user_profile.create_bet(bet, user_bet.wagered_amount, user_bet.wagered_option)
            return redirect('bookmaker:place_bet', bet_id=bet.id)
    else:
        form = UserBetForm()

    return render(request, "place_bet.html", {'form': form, 'bet': bet})
