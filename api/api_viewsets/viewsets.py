from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from api.utils import paginate_queryset

from .serializers import LoginSerializer, RegisterSerializer, UserListSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def authenticate(request):
  serializer = LoginSerializer(data=request.data)
  serializer.is_valid(raise_exception=True)
  user = serializer.validated_data

  refresh = RefreshToken.for_user(user)

  return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
  serializer = RegisterSerializer(data=request.data)
  serializer.is_valid(raise_exception=True)
  user = serializer.save()

  refresh = RefreshToken.for_user(user)
  access = refresh.access_token

  return Response({
      'message': 'User registered successfully.',
      'user': {
          'id': user.id,
      },
      'tokens': {
          'refresh': str(refresh),
          'access': str(access),
      }
  }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
  users = User.objects.all().order_by('id')
  paginator, paginated_users = paginate_queryset(users, request)
  serializer = UserListSerializer(paginated_users, many=True)
  
  return paginator.get_paginated_response(serializer.data)