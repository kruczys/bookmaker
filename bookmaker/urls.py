from django.urls import path, include

from . import views

app_name = 'bookmaker'
urlpatterns = [
    path("", views.index, name="index"),
    path("auth/signup", views.SignupView.as_view(), name="signup"),
    path("<int:bet_id>/comments/", views.comment_section, name="comments"),
]
