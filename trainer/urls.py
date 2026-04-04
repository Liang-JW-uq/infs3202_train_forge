from django.urls import path, include

from .views import index_view, home_view, query_view, client_view, account_view

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", index_view.index, name="index"),
    path("index/", index_view.index, name="index"),


    # For Django Login + Register Authentication
    path("login/", account_view.login_page, name="login"),
    path("register/", account_view.register_page, name="register"),
    path("", include("django.contrib.auth.urls")),

    # This is for the Trainer app onwards
    path("home/", login_required(home_view.home), name="home"),
]