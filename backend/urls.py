from django.urls import path, include

from .views import subscription_view

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", subscription_view.subscription_list, name="subscription_list"),
    path("list/", subscription_view.subscription_list, name="subscription_list"),

]