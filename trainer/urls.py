from django.urls import path, include, reverse_lazy

from .views import index_view, home_view, query_view, client_view, account_view
from .views import tag_view, exercise_view, appointment_view, workout_view
from .views import ai_view

from django.contrib.auth.decorators import login_required

from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path("", index_view.index, name="index"),
    path("index/", index_view.index, name="index"),

    # This is for social-auth-django, which allows login via 3rd-party accounts like Gmail, Facebook, etc
    #####
    # social-auth-django provides the 'social:begin' namespace
    path('social-auth/', include('social_django.urls', namespace='social')),

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

    path("tag/info/", tag_view.get_trainer_tags, name="get_trainer_tags"),

    path("exercise/", login_required(exercise_view.exercise_list), name="exercise_list"),
    path("exercise/add/", login_required(exercise_view.exercise_add), name="exercise_add"),
    path("exercise/edit/<int:pk>/", login_required(exercise_view.exercise_edit), name="exercise_edit"),
    path("exercise/delete/<int:pk>/", login_required(exercise_view.exercise_delete), name="exercise_delete"),

    path('exercises/tags/<str:tag_ids>/', exercise_view.get_exercises_by_tags, name='exercises_by_tags'),

    path("client/", login_required(client_view.client_list), name="client_list"),
    path("client/add/", login_required(client_view.client_add), name="client_add"),
    path("client/edit/<int:pk>/", login_required(client_view.client_edit), name="client_edit"),
    path("client/delete/<int:pk>/", login_required(client_view.client_delete), name="client_delete"),

    # path("client/info/<int:pk>/", client_view.get_client_info, name="get_client_info"),
    path("client/info/", client_view.get_client_info, name="get_client_info"),

    path("appointment/", login_required(appointment_view.appointment_list), name="appointment_list"),
    path("appointment/add/", login_required(appointment_view.appointment_add), name="appointment_add"),
    path("appointment/edit/<int:pk>/", login_required(appointment_view.appointment_edit), name="appointment_edit"),
    path("appointment/delete/<int:pk>/", login_required(appointment_view.appointment_delete), name="appointment_delete"),

    path("appointment/calendar", login_required(appointment_view.appointment_calendar), name="appointment_calendar"),
    path("appointment/calendar/events", login_required(appointment_view.get_trainer_appointments), name="get_trainer_appointments"),

    path("workout/", login_required(workout_view.workout_list), name="workout_list"),
    path("workout/add/", login_required(workout_view.workout_add), name="workout_add"),
    path("workout/edit/<int:pk>/", login_required(workout_view.workout_edit), name="workout_edit"),
    path("workout/delete/<int:pk>/", login_required(workout_view.workout_delete), name="workout_delete"),
    path("workout/pending/", login_required(workout_view.get_pending_workouts), name="get_pending_workouts"),

    path("ai/generate/<str:prompt>", ai_view.ask, name="ai_generate"),
    path("ai/generate2/<str:prompt>", ai_view.ask2, name="ai_generate"),
    path("ai/generate3/<str:prompt>", ai_view.ask3, name="ai_generate"),
    path("ai/generate/workout/<int:client_id>/<int:no_of_exercises>", ai_view.generate_workout, name="ai_generate_workout")
]