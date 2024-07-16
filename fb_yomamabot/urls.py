# yomamabot/fb_yomamabot/urls.py
from django.urls import path
from .views import YoMamaBotView, chat_widget, send_message

urlpatterns = [
    path('webhook/', YoMamaBotView.as_view(), name='webhook'),
    path('chat_widget/', chat_widget, name='chat_widget'),
    path('send_message/', send_message, name='send_message'),
]



# # yomamabot/fb_yomamabot/urls.py
# from django.urls import path
# from .views import YoMamaBotView

# urlpatterns = [
#     path('webhook', YoMamaBotView.as_view(), name='webhook'),
# ]
