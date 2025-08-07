from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

from api.utils import paginate_queryset

from .serializers import LoginSerializer, RegisterSerializer, UpdateUserSerializer, UserListSerializer

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

@api_view(['POST'])
@permission_classes([AllowAny])
def verify(request):
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({'detail': 'Authorization header missing or malformed.'}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ')[1]

    jwt_authenticator = JWTAuthentication()
    try:
        jwt_authenticator.get_validated_token(token)
        return Response({
            'valid': True,
        }, status=status.HTTP_200_OK)
    except AuthenticationFailed as e:
        return Response({'valid': False, 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createUser(request):
  serializer = RegisterSerializer(data=request.data)
  serializer.is_valid(raise_exception=True)
  user = serializer.save()

  return Response({
      'message': 'User registered successfully.',
      'user': {
          'id': user.id,
      }
  }, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    user_id = request.data['user_id']
    try:
      user = User.objects.get(pk=user_id)
      serializer = UpdateUserSerializer(user, data=request.data, partial=True)
      if serializer.is_valid():
          serializer.save()
          return Response({'message': 'User updated successfully'}, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
  user_id = request.data['user_id']
  try:
    user = User.objects.get(pk=user_id)
    user.delete()
    return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
  except User.DoesNotExist:
    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
