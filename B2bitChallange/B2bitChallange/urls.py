"""
Definition of urls for B2bitChallange.
"""

from datetime import datetime
from django.urls import path, include
from app import forms, views
from .router import router
from app.views import login, user_info


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login', login),
    path('api/user_info', user_info),
]
