from django.contrib import admin

from .models import UserProfile, Bet, Comment, UserBet

admin.site.register(UserProfile)
admin.site.register(Bet)
admin.site.register(Comment)
admin.site.register(UserBet)
