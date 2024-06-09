from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from utils.custom_response import CustomResponse

from .serializers import (
    PostBaseSerializer,
    PostDetailSerializer,
)
from .models import Post
import logging

logger = logging.getLogger(__name__)


class GetAllPosts(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PostDetailSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def __get_user(self, id):
        return Post.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.__get_user(id), many=True)
        kwargs["data"] = serializer.data
        response = CustomResponse(**kwargs)
        return response.success_response()

class GetPostDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostDetailSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def __get_user(self, id):
        return Post.objects.filter(id=id)

    def get(self, request, id, *args, **kwargs):
        serializer = self.get_serializer(self.__get_user(id), many=True)
        kwargs["data"] = serializer.data
        response = CustomResponse(**kwargs)
        return response.success_response()


class CreatePostView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostBaseSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        serializer = PostBaseSerializer(data)
        kwargs["data"] = serializer.data
        response = CustomResponse(**kwargs)
        return response.success_response()