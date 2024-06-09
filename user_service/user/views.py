
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from utils.custom_response import CustomResponse

from .serializers import (
    UserAccountSerializer,
    UserAccountUpdateSerializer,
    TokenSerializer,
)
from .models import User
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class TokenLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()
        serializer = UserAccountSerializer(user)

        kwargs["user"] = serializer.data
        kwargs["token"] = token.key
        response = CustomResponse(**kwargs)
        print(response)
        return response.success_response()


class TokenLogoutView(APIView):
    serializer_class = TokenSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountRegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserAccountSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()
        serializer = UserAccountSerializer(user)
        kwargs["user"] = serializer.data
        kwargs["token"] = str(token[0])
        response = CustomResponse(**kwargs)
        return response.success_response()


class UpdateUserAccountView(APIView):
    serializer_class = UserAccountUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            instance=self.request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = UserAccountSerializer(user)
        logger.info(f"User details ${serializer.data}")
        kwargs["user"] = serializer.data
        response = CustomResponse(**kwargs)
        return response.success_response()


class GetUserDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAccountSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def __get_user(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        user = self.__get_user(id)
        if(user):
            serializer = self.get_serializer(user)
            kwargs["data"] = serializer.data
            response = CustomResponse(**kwargs)
            return response.success_response()
        kwargs["data"] = "user does not exist."
        response = CustomResponse(**kwargs)
        return response.failed_response()
     
class GetAllUsers(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAccountSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def __get_user(self):
        return User.objects.filter(is_active=True)
       

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.__get_user(),many=True)
        kwargs["data"] = serializer.data
        response = CustomResponse(**kwargs)
        return response.success_response()
        kwargs["data"] = "user does not exist."
        response = CustomResponse(**kwargs)
        return response.failed_response() 