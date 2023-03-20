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

        return Response({"success": True})
