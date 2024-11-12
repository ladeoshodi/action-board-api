import jwt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import ValidationError
from .serializers.common import UserSerializer
from .serializers.populated import PopulatedUserSerializer
from .serializers.auth import AuthUserSerializer

from drf_spectacular.utils import extend_schema, OpenApiRequest, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

User = get_user_model()


class RegisterView(APIView):
    @extend_schema(
        tags=["User"],
        request=AuthUserSerializer,
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.STR,
                examples=[OpenApiExample(
                    name="Registration Successful",
                    value={"message": "Registration Successful"})]
            )}
    )
    def post(self, request):
        user_to_create = AuthUserSerializer(data=request.data)

        if user_to_create.is_valid():
            user_to_create.save()
            return Response({"message": "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):

    @extend_schema(
        tags=["User"],
        request=OpenApiRequest(
            request=OpenApiTypes.OBJECT,
            examples=[OpenApiExample(
                name="Login Example", value={"email": "email@example.com", "password": "secure_password"}
            )]),
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[OpenApiExample(name="Login Successful", value={
                    "token": "secure_token",
                    "message": "Login successful"
                })]
            )}
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail="Invalid Credentials")

        if not user_to_login.check_password(password):
            raise PermissionDenied(detail="Invalid Credentials")

        if not user_to_login.is_active:
            raise PermissionDenied(detail="User account is inactive")

        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode({"pk": user_to_login.id, "exp": int(
            dt.timestamp())}, settings.SECRET_KEY, algorithm="HS256")

        return Response({"token": token, "message": f"Welcome back {user_to_login.username}"})


class UserDetailView(APIView):
    permission_classes = IsAuthenticated,

    @extend_schema(
        tags=["User"],
        responses=PopulatedUserSerializer,
    )
    def get(self, request):
        try:
            serialized_user = PopulatedUserSerializer(request.user)
            return Response(serialized_user.data)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @extend_schema(
        tags=["User"],
        request=AuthUserSerializer,
        responses={202: PopulatedUserSerializer},
    )
    def put(self, request):
        if "password" in (request.data.keys()):
            updated_user = AuthUserSerializer(
                request.user, data=request.data, partial=True)
        else:
            updated_user = UserSerializer(
                request.user, data=request.data, partial=True)

        try:
            updated_user.is_valid(raise_exception=True)
            updated_user.save()
            return Response(updated_user.data, status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return Response(updated_user.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @extend_schema(
        tags=["User"],
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
