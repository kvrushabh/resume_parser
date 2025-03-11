from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path("signup", views.handlesignup, name="handlesignup"),
    path("login", views.handleLogin, name="login"),
    path("logout", views.handleLogout, name="handlelogout"),

    # for email verification
    path("verify/<auth_token>", views.email_verify, name="verify"),

    # for reset password
    path("forget-password", views.forgetpassword, name="forget-password"),
    path("change-password/<token>/", views.changepassword, name="change-password"),

]
