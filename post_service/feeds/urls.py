from . import views
from django.urls import path

app_name = 'post'

urlpatterns = [
    path("all/", views.GetAllPosts.as_view(), name="all-posts"),
    path("detail/<str:id>/", views.GetPostDetail.as_view(), name="post-detail"),
    path("create/", views.CreatePostView.as_view(), name="create-post"),
]
