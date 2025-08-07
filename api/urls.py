from django.urls import path
from .api_viewsets import viewsets

urlpatterns = [
  path('login/', viewsets.authenticate),
  path('register/', viewsets.register),
  path('view/', viewsets.get_users),
]