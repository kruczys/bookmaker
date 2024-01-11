from django.test import TestCase

from .models import UserProfile, Bet, Comment


class BetModelTestCase(TestCase):
    def test_correct_total_money(self):
        bet = Bet(win_money_wagered=10, draw_money_wagered=10, lose_money_wagered=10)
        self.assertEqual(bet.get_total_money_wagered(), 30)

    def test_correct_win_odds(self):
        bet = Bet(win_money_wagered=10, draw_money_wagered=10, lose_money_wagered=10)
        correct_odds = 30 / 10
        self.assertEqual(bet.get_win_odds(), correct_odds)

