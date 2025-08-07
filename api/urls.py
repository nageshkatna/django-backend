from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_viewsets import viewsets

urlpatterns = [
  path('login/', viewsets.authenticate),
  path('register/', viewsets.register),
  path('verify/', viewsets.verify),
  path('view/', viewsets.get_users),
  path('createUser/', viewsets.createUser),
  path('updateUser/', viewsets.updateUser),
  path('deleteUser/', viewsets.deleteUser),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]