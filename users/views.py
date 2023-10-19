from ast import IsNot
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ParseError
from . import models
from . import serializers

# Create your views here.
class UserView(APIView):
    def get(self, request):
        users = models.User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)


class SignUpView(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is None or password is None:
            raise ParseError("Username/Password not set")

        user = models.User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        serializer = serializers.UserSerializer(user)

        return Response(serializer.data)
