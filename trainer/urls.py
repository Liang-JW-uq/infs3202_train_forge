from django.urls import path, include, reverse_lazy

from .views import index_view, home_view, query_view, client_view, account_view
from .views import tag_view, exercise_view

from django.contrib.auth.decorators import login_required

from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path("", index_view.index, name="index"),
    path("index/", index_view.index, name="index"),


    # For Django Login + Register Authentication
    # path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    # path("admin/", admin.site.urls),
    path("login/", account_view.login_page, name="login"),
    path("register/", account_view.register_page, name="register"),
    path("", include("django.contrib.auth.urls")),
    

    # This is for the Trainer app onwards
    path("home/", login_required(home_view.home), name="home"),

    path("tag/", login_required(tag_view.tag_list), name="tag_list"),
    path("tag/add/", login_required(tag_view.tag_add), name="tag_add"),
    path("tag/edit/<int:pk>/", login_required(tag_view.tag_edit), name="tag_edit"),
    path("tag/delete/<int:pk>/", login_required(tag_view.tag_delete), name="tag_delete"),

    path("exercise/", login_required(exercise_view.exercise_list), name="exercise_list"),
    path("exercise/add/", login_required(exercise_view.exercise_add), name="exercise_add"),
    path("exercise/edit/<int:pk>/", login_required(exercise_view.exercise_edit), name="exercise_edit"),
    path("exercise/delete/<int:pk>/", login_required(exercise_view.exercise_delete), name="exercise_delete"),

    path("client/", login_required(client_view.client_list), name="client_list"),
    path("client/add/", login_required(client_view.client_add), name="client_add"),
    path("client/edit/<int:pk>/", login_required(client_view.client_edit), name="client_edit"),
    path("client/delete/<int:pk>/", login_required(client_view.client_delete), name="client_delete"),
]