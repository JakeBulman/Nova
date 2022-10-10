from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('register_user', views.register_user, name="register_user"),
    path('logout_users', views.logout_user, name="logout"),
]