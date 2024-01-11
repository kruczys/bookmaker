from django.urls import path

from . import views
from .views import IndexListView

app_name = 'bookmaker'
urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path("<int:bet_id>/comments", views.comment_section, name="comments")
]
