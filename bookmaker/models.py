from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)

    def __str__(self):
        return self.nickname


class Bet(models.Model):
    bet_text = models.CharField(max_length=200)
    resolve_date = models.DateTimeField("Date resolved")
    win_money_wagered = models.IntegerField(default=0)
    draw_money_wagered = models.IntegerField(default=0)
    loose_money_wagered = models.IntegerField(default=0)
    possible_to_draw = models.BooleanField(default=False)

    def __str__(self):
        return self.bet_text

    def get_total_money_wagered(self):
        return self.win_money_wagered + self.draw_money_wagered + self.loose_money_wagered

    def get_win_odds(self):
        if not self.win_money_wagered:
            return 0
        return round(self.get_total_money_wagered() / self.win_money_wagered, 2)

    def get_draw_odds(self):
        if not self.draw_money_wagered:
            return 0
        return round(self.get_total_money_wagered() / self.draw_money_wagered, 2)

    def get_loose_ods(self):
        if not self.loose_money_wagered:
            return 0
        return round(self.get_total_money_wagered() / self.loose_money_wagered, 2)


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date published")
    likes = models.IntegerField(default=0)
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")

    def __str__(self):
        return self.comment_text
