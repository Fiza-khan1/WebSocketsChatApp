from django.shortcuts import render, redirect
from .models import Group, Chat
from channels.layers import get_channel_layer
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token


def index(request, groupname):
    group = Group.objects.filter(groupName=groupname).first()
    if not group:
        group = Group.objects.create(groupName=groupname)

    chats = Chat.objects.filter(Gname=group)
    print("Chats:", list(chats))

    return render(request, 'app/index.html', {'groupname': group.groupName, 'chats': chats})


def msgfromoutside(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'new',  # Ensure this matches the group name
        {
            'type': 'chat.message',
            'text': 'Message from outside the consumer'  # Ensure 'text' key is used
        }
    )

    return HttpResponse("Message from outside the consumer")


# User registration view
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate a token for the newly created user
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'message': 'User registered successfully',
                    'token': token.key  # Include the token in the response
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User login view

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# You might also want to add a logout view
class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
