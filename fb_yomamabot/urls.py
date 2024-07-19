# yomamabot/fb_yomamabot/urls.py
from django.urls import path
from .views import YoMamaBotView, chat_widget, send_message, fetch_pages



   


urlpatterns = [
    path('webhook', YoMamaBotView.as_view(), name='webhook'),
    path('chat_widget', chat_widget, name='chat_widget'),
    path('fetch_pages/', fetch_pages, name='fetch_pages'),
    path('send_message/', send_message, name='send_message'),
]


