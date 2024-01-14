from random import randint

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username

    def reduce_wallet(self, amount):
        if self.wallet < amount:
            raise ValueError("Insufficient funds.")
        self.wallet -= amount
        self.user.save()
        self.save()

    def create_bet(self, bet, wagered_amount, wagered_option):
        user_bet = UserBet.objects.create(
            user=self,
            bet=bet,
            wagered_amount=wagered_amount,
            wagered_option=wagered_option
        )
        self.reduce_wallet(wagered_amount)
        return user_bet


def handle_user_profile_saving(instance):
    instance.userprofile.save_with_user()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Bet(models.Model):
    bet_text = models.CharField(max_length=200)
    resolve_date = models.DateTimeField("Date resolved")
    win_money_wagered = models.IntegerField(default=0)
    draw_money_wagered = models.IntegerField(default=0)
    loose_money_wagered = models.IntegerField(default=0)
    possible_to_draw = models.BooleanField(default=False)
    result = randint(0, 2)

    def __str__(self):
        return self.bet_text

    def get_total_money_wagered(self):
        return self.win_money_wagered + self.draw_money_wagered + self.loose_money_wagered

    def get_win_odds(self):
        if not self.win_money_wagered:
            return 1
        return round(self.get_total_money_wagered() / self.win_money_wagered, 2)

    def get_draw_odds(self):
        if not self.draw_money_wagered:
            return 1
        return round(self.get_total_money_wagered() / self.draw_money_wagered, 2)

    def get_loose_odds(self):
        if not self.loose_money_wagered:
            return 1
        return round(self.get_total_money_wagered() / self.loose_money_wagered, 2)

    def is_resolved(self):
        return timezone.now() >= self.resolve_date


class UserBet(models.Model):
    WAGERED_OPTION_CHOICES = [
        (0, "Win"),
        (1, "Draw"),
        (2, "Loose"),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    wagered_amount = models.IntegerField(default=0)
    wagered_option = models.IntegerField(choices=WAGERED_OPTION_CHOICES)
    is_won = models.BooleanField(default=False)

    def check_and_resolve(self):
        if self.bet.is_resolved() and self.wagered_option == self.bet.result:
            self.is_won = True
            self.calculate_reward()

    def calculate_reward(self):
        if self.wagered_option == 0:
            reward = self.wagered_amount * self.bet.get_win_odds()
        elif self.wagered_option == 1:
            reward = self.wagered_amount * self.bet.get_draw_odds()
        else:
            reward = self.wagered_amount * self.bet.get_loose_odds()

        self.user.wallet = max(self.user.wallet + reward, 0)
        self.user.save()


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date published")
    likes = models.IntegerField(default=0)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")

    def __str__(self):
        return self.comment_text

    def increment_likes(self):
        self.likes += 1
        self.user.save()
        self.save()
