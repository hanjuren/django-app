import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated

from accounts.services import SignUpService, SignInService, SignOutService, ChangePasswordService
from accounts.serializers.validation_serializers import SignUpSerializer, SignInSerializer, ChangePasswordSerializer

from users.serializers.response_serializers import PrivateUserSerializer


class SignUp(APIView):
    """
    Sign-Up API
    """

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = SignUpService(serializer.validated_data)
            user = service.execute()

            Response(
                PrivateUserSerializer(user).data,
                status=HTTP_201_CREATED,
            )
        except RuntimeError as err:
            logging.error(err)
            return Response(
                {"message": err.args[0]},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


class SignIn(APIView):
    """
    Sign-In API
    """

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = SignInService(request, serializer.validated_data)
            user = service.execute()

            return Response(
                PrivateUserSerializer(user).data,
                status=HTTP_201_CREATED,
            )
        except RuntimeError as err:
            logging.error(err)
            return Response(
                {"message": err.args[0]},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


class SignOut(APIView):
    """
    Sign-Out API
    """

    def post(self, request):
        try:
            service = SignOutService(request)
            service.execute()

            return Response(status=HTTP_204_NO_CONTENT)
        except RuntimeError as err:
            logging.error(err)
            return Response(
                {"message": err.args[0]},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePassword(APIView):
    """
    User Change password
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            current_user = request.user
            service = ChangePasswordService(current_user, serializer.validated_data)
            user = service.execute()

            return Response(PrivateUserSerializer(user).data)
        except RuntimeError as err:
            logging.error(err)
            return Response(
                {"message": err.args[0]},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
