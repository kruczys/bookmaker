from django.urls import path, include

from . import views

app_name = 'bookmaker'
urlpatterns = [
    path("", views.index, name="index"),
    path("auth/signup", views.SignupView.as_view(), name="signup"),
    path("<int:bet_id>/comments/", views.comment_section, name="comments"),
    path("create_bet/", views.create_bet, name="create_bet"),
    path("<int:bet_id>/place_bet/", views.place_bet, name="place_bet"),
    # path("create_comment/", views.create_comment, name="create_comment"),
]
