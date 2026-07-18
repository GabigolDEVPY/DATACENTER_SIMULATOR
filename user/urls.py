from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserLogoutView, GetBalanceView

app_name = "user"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    
    path("get-balance/", GetBalanceView.as_view(), name="get_balance"),
    ]