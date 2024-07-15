# yomamabot/fb_yomamabot/urls.py
from django.urls import path
from .views import YoMamaBotView

urlpatterns = [
    path('webhook', YoMamaBotView.as_view(), name='webhook'),
]
