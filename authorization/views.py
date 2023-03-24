from django.contrib.auth import authenticate
from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from users import serializers, models


class SignUp(APIView):
    """
    user sing up
    """
    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()

        result = {"success": True}
        return Response(result, status=status.HTTP_201_CREATED)


class SignIn(APIView):
    """
    user sign in
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise exceptions.ParseError

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if not user:
            raise exceptions.NotFound(detail="Not Found User.")

        access_token = user.gen_jwt_token()
        result = {
            "success": True,
            "access_token": access_token,
        }
        return Response(result, status=status.HTTP_201_CREATED)
