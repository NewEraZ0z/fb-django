# yomamabot/fb_yomamabot/urls.py
from django.urls import path
from . import  views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('webhook', views.YoMamaBotView.as_view(), name='webhook'),
    path('send_message/', views.send_message, name='send_message'),
    path('conversations/', views.get_conversations, name='get_conversations'),
    path('messages/<str:conversation_id>/', views.get_messages, name='get_messages'),
    path('message/<str:message_id>/', views.get_message_details, name='get_message_details'),
]
