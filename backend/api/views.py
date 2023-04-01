from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from structure.models import Org

from .serializers import *


class OrgAPICreate(generics.CreateAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer


class OrgAPIDetail(generics.RetrieveAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializerRestricted


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'detail': 'Logged in successfully.'})
            else:
                print(f"{user}:{email}:{password}")
                return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
