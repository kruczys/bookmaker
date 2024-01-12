from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import UserProfile, Bet, Comment


class BetModelTestCase(TestCase):
    def test_correct_total_money(self):
        bet = Bet.objects.create(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10,
                                 resolve_date=timezone.now())
        self.assertEqual(bet.get_total_money_wagered(), 30)

    def test_correct_win_odds(self):
        bet = Bet.objects.create(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10,
                                 resolve_date=timezone.now())
        correct_odds = 30 / 10
        self.assertEqual(bet.get_win_odds(), correct_odds)

    def test_correct_draw_odds(self):
        bet = Bet.objects.create(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10,
                                 resolve_date=timezone.now())
        correct_odds = 30 / 10
        self.assertEqual(bet.get_draw_odds(), correct_odds)

    def test_correct_lose_odds(self):
        bet = Bet.objects.create(win_money_wagered=10, draw_money_wagered=10, loose_money_wagered=10,
                                 resolve_date=timezone.now())
        correct_odds = 30 / 10
        self.assertEqual(bet.get_loose_odds(), correct_odds)

    def test_no_money_wagered_win_odds(self):
        bet = Bet.objects.create(win_money_wagered=0, resolve_date=timezone.now())
        self.assertEqual(bet.get_win_odds(), 1)

    def test_no_money_wagered_draw_odds(self):
        bet = Bet.objects.create(draw_money_wagered=0, resolve_date=timezone.now())
        self.assertEqual(bet.get_win_odds(), 1)

    def test_no_money_wagered_lose_odds(self):
        bet = Bet.objects.create(loose_money_wagered=0, resolve_date=timezone.now())
        self.assertEqual(bet.get_loose_odds(), 1)

    def test_resolved_bet(self):
        bet = Bet.objects.create(resolve_date=timezone.now() + timezone.timedelta(days=1))
        self.assertEqual(bet.is_resolved(), True)

    def test_unresolved_bet(self):
        bet = Bet.objects.create(resolve_date=timezone.now() - timezone.timedelta(days=1))
        self.assertEqual(bet.is_resolved(), False)


class UserModelTestCase(TestCase):
    def test_reduce_too_much_money(self):
        user = User.objects.create_user(username="test", password="<PASSWORD>")
        user_profile = UserProfile.objects.get(user=user)
        with self.assertRaises(ValueError):
            user_profile.reduce_wallet(1050)

    def test_reduce_wallet_correctly(self):
        reduce_amount = 50
        user = User.objects.create_user(username="test", password="<PASSWORD>")
        user_profile = UserProfile.objects.get(user=user)
        user_profile.reduce_wallet(reduce_amount)
        self.assertEqual(1000 - reduce_amount, user_profile.wallet)


class CommentModelTestCase(TestCase):
    def test_increment_likes(self):
        user = User.objects.create_user(username="test", password="<PASSWORD>")
        user_profile = UserProfile.objects.get(user=user)
        comment = Comment.objects.create(pub_date=timezone.now(), user=user_profile)
        likes_before = comment.likes
        comment.increment_likes()
        likes_after = comment.likes
        self.assertEqual(likes_before + 1, likes_after)


class IndexViewTestCase(TestCase):
    def test_load_main_page(self):
        response = self.client.get(reverse("bookmaker:index"))
        self.assertEqual(response.status_code, 200)

    def test_no_bets_found(self):
        response = self.client.get(reverse("bookmaker:index"))
        self.assertContains(response, "No bets in database")
        self.assertQuerysetEqual(response.context["bets_list"], [])

    def test_render_bets_page(self):
        bet = Bet.objects.create(bet_text="bet", resolve_date=timezone.now())
        response = self.client.get(reverse("bookmaker:index"))
        self.assertContains(response, bet.bet_text)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["bets_list"], [bet])


class CommentSectionViewTestCase(TestCase):
    def test_load_comments_section(self):
        bet = Bet.objects.create(bet_text="bet", resolve_date=timezone.now())
        response = self.client.get(reverse("bookmaker:comments", args=(bet.id,)))
        self.assertEqual(response.status_code, 200)

    def test_load_wrong_id(self):
        response = self.client.get(reverse("bookmaker:comments", args=(1000,)))
        self.assertEqual(response.status_code, 404)
