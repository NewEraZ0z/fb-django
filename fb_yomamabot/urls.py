# yomamabot/fb_yomamabot/urls.py
from django.urls import path
from . import  views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('webhook', views.YoMamaBotView.as_view(), name='webhook'),
]
