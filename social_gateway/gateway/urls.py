from . import views
from django.urls import path

app_name = 'gateway'

urlpatterns = [
    path("all-posts/", views.GetAllPosts.as_view(), name="all-posts"),
    path("post-detail/<str:id>/", views.GetPostDetail.as_view(), name="post-detail"),
    path("create-post/", views.CreatePostView.as_view(), name="create-post"),

    path("login/", views.LoginView.as_view(), name="token-login"),
    path("register/", views.UserRegistrationView.as_view(), name="account-registration"),
]
