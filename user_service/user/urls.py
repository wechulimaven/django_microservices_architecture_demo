from . import views
from django.urls import path

app_name = 'user'

urlpatterns = [
    path("login/", views.TokenLoginView.as_view(), name="token-login"),
    path("logout/", views.TokenLogoutView.as_view(), name="token-logout"),
    path("register/", views.AccountRegistrationView.as_view(), name="account-registration"),
    path("update-account/", views.UpdateUserAccountView.as_view(), name="update-account-registration"),
    path("detail/<str:id>/", views.GetUserDetail.as_view(), name='user-detail'),
    path("all/", views.GetAllUsers.as_view(), name='all'),

]
