# yomamabot/yomamabot/urls.py
from django.urls import path, re_path, include
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('', include('fb_yomamabot.urls')),
]
