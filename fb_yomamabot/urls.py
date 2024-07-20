# yomamabot/fb_yomamabot/urls.py
from django.urls import path
from .views import YoMamaBotView, chat_widget, send_message, fetch_pages, fetch_users



urlpatterns = [
    path('webhook', YoMamaBotView.as_view(), name='webhook'),
    path('chat_widget', chat_widget, name='chat_widget'),
    path('fetch_pages/', fetch_pages, name='fetch_pages'),
     path('fetch_users/', fetch_users, name='fetch_users'),
    path('send_message/', send_message, name='send_message'),
]


