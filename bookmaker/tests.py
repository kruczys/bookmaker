from django.test import TestCase

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
        self.assertEqual(bet.get_lose_odds(), correct_odds)

    def test_incorrect_win_odds(self):
        bet = Bet(win_money_wagered=0)
        self.assertEqual(bet.get_win_odds(), 0)

    def test_incorrect_draw_odds(self):
        bet = Bet(draw_money_wagered=0)
        self.assertEqual(bet.get_win_odds(), 0)

    def test_incorrect_lose_odds(self):
        bet = Bet(loose_money_wagered=0)
        self.assertEqual(bet.get_lose_odds(), 0)
