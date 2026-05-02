from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Exists, OuterRef
from orm.models import UserTrainer, Tag, Exercise, Client, Workout, WorkoutExercise

def home(request):
    userTrainer = get_object_or_404(UserTrainer, pk=request.user.id)
    tags_count = Tag.objects.filter(trainer=userTrainer).count()
    exercise_count = Exercise.objects.filter(trainer=userTrainer).count()
    client_count = Client.objects.filter(trainer=userTrainer).count()
    workout_count = Workout.objects.filter(trainer=userTrainer).count()

    workouts = Workout.objects.filter(trainer=userTrainer)

    ## AI ASSISTED WITH INTRODUCING THE IDEA OF SUBQUERIES
    any_done = WorkoutExercise.objects.filter(
        workout=OuterRef('pk'),
        is_done=True
    )

    workouts = workouts.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(is_completed=True)),
        ## AI ASSISTED WITH STRUCTURING QUERIES
        not_started=Count(
            'id', 
            filter=Q(is_completed=False) & ~Exists(any_done)
        ),
        in_progress=Count(
            'id', 
            filter=Q(is_completed=False) & Exists(any_done)
        )
    )

    # annotate - will gives us a group by client
    workout_agg = {"high": 0, "medium": 0, "low": 0}

    clients_workouts = Client.objects.filter(trainer=userTrainer).annotate(
        total=Count('workouts')
    )                                       # left outer join
    for client in clients_workouts:
        if client.total >= 5:
            workout_agg['high'] = workout_agg["high"] + 1
        elif client.total >= 1:
            workout_agg["medium"] = workout_agg["medium"] + 1
        else:
            workout_agg["low"] = workout_agg["low"] + 1

    summary = {
        "tags_count": tags_count,
        "exercise_count": exercise_count,
        "client_count": client_count,
        "client_workouts": workout_agg,
        "workouts": workouts,
    }

    return render(request, "trainer/home.html", {"summary": summary})