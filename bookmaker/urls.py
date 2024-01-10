from django.urls import path

from . import views

app_name = 'bookmaker'
urlpatterns = [
    path("", views.index, name="index"),
]
