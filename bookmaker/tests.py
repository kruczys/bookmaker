from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse

from .models import UserProfile, Bet, Comment


class BetModelTestCase(TestCase):
    def test_correct_total_money(self):
        bet = Bet(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10)
        self.assertEqual(bet.get_total_money_wagered(), 30)

    def test_correct_win_odds(self):
        bet = Bet(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10)
        correct_odds = 30 / 10
        self.assertEqual(bet.get_win_odds(), correct_odds)

    def test_correct_draw_odds(self):
        bet = Bet(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10)
        correct_odds = 30 / 10
        self.assertEqual(bet.get_draw_odds(), correct_odds)

    def test_correct_lose_odds(self):
        bet = Bet(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10)
        correct_odds = 30 / 10
        self.assertEqual(bet.get_loose_odds(), correct_odds)

    def test_incorrect_win_odds(self):
        bet = Bet(win_money_wagered=0)
        self.assertEqual(bet.get_win_odds(), 0)

    def test_incorrect_draw_odds(self):
        bet = Bet(draw_money_wagered=0)
        self.assertEqual(bet.get_win_odds(), 0)

    def test_incorrect_lose_odds(self):
        bet = Bet(loose_money_wagered=0)
        self.assertEqual(bet.get_loose_odds(), 0)

    def test_reduce_too_much_money(self):
        user = User(username="", password="<PASSWORD>")
        user_profile = UserProfile(user=user)
        with self.assertRaises(ValueError):
            user_profile.reduce_wallet(1050)

    def test_reduce_wallet_correctly(self):
        wallet_amount = 100
        reduce_amount = 50
        user = User(username="", password="<PASSWORD>")
        user_profile = UserProfile(user=user, wallet=wallet_amount)
        user_profile.reduce_wallet(reduce_amount)
        self.assertEqual(wallet_amount - reduce_amount, user_profile.wallet)

    def test_no_bets_found(self):
        response = self.client.get(reverse("bookmaker:index"))
        self.assertContains(response, "No bets in database")
        self.assertQuerysetEqual(response.context["bets_list"], [])

    def test_load_main_page(self):
        response = self.client.get(reverse("bookmaker:index"))
        self.assertEqual(response.status_code, 200)



