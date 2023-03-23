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
        access_token = user.gen_jwt_token()

        result = {
            "success": True,
            "token": access_token,
        }

        return Response(result, status=status.HTTP_201_CREATED)
