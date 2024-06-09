from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from services.post_service import PostService
from utils.custom_response import CustomResponse

from .serializer import (
    UserSerializer,
    PostSerializer,
LoginSerializer,
)
import logging

logger = logging.getLogger(__name__)


class GetAllPosts(APIView):
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def __get_post(self):
        post_service = PostService()
        _, post =post_service.get_feeds()

        return post

    def get(self, request, *args, **kwargs):
        kwargs["data"] = self.__get_post()
        response = CustomResponse(**kwargs)
        return response.success_response()

class GetPostDetail(APIView):
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def __get_user(self, id):
        post_service = PostService()
        _, post =post_service.get_feed_detail(id)

        return post

    def get(self, request, id, *args, **kwargs):
        kwargs["data"] = self.__get_user(id)
        response = CustomResponse(**kwargs)
        return response.success_response()
    
class CreatePostView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        kwargs["data"] = data
        response = CustomResponse(**kwargs)
        return response.success_response()

class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        kwargs["data"] = user
        response = CustomResponse(**kwargs)
        return response.success_response()


class UserRegistrationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        kwargs["data"] = user
        response = CustomResponse(**kwargs)
        return response.success_response()