# from django.shortcuts import render, redirect
# from django.db.models import Aggregate, Avg
# from orm.models import Trainer, Client, Tag, Exercise, TagExercise, Workout, WorkoutExercise

# def query(request):
#     # #1 - { GET ALL }
#     # trainers = Trainer.objects.all()
#     # print(trainers.query)
#     # for t in trainers:
#     #     print(f"{t.name} - {t.email}")

#     # #2 - { FILTER BY ID }
#     # clients = Client.objects.filter(trainer__id=1)
#     # for c in clients:
#     #     print(f"{c.name} - {c.trainer.id} - {c.trainer.name}")

#     # #3 - { CHAIN/JOIN GET }
#     # trainer = Trainer.objects.get(id=1)
#     # clients = trainer.clients.all()
#     # for c in clients:
#     #     print(f"{c.name} - {c.trainer.id} - {c.trainer.name}")

# # ------------------------------------------------------------------------------------

#     # # [ Basic Retrieval + Extraction ]
#     # # 1 - { Get Single object }
#     # trainer = Trainer.objects.get(id=2)
#     # print(f"{trainer.name} - {trainer.email} - {trainer.contact_no}")

#     # # 2 - { Fetch All Records }
#     # clients = Client.objects.all()
#     # for c in clients:
#     #     print(f"{c.name}:\n\tAge: {c.age}\n\tEmail: {c.email}")

#     # # 3 - { Limit & Offset (Slicing, Only retrieve first/last 5 items) }
#     # tags = Tag.objects.all()[1:4] # This gives first 4 results
#     #         # tags = Tag.objects.all()[1:4]   <--- Returns results INDEX (not id) 1 to 3 (Inclusive:Exclusive)
#     #         # There is NO NEGATIVE INDEXING by default; cannot ask for "last 5 results", need to explicitly state two indexes... UNLESS
#     #         # use this:
#     #                 # tags = Tag.objects.order_by('-id')[:5]
#     #                     # Order by descending first ('-id'), then take the first 5 from that
#     # for t in tags:
#     #     print(f"{t.name}")

#     # # 4 - { Specific Column Selection }
#     # exercises = Exercise.objects.all().values("trainer__name", "name", "default_reps")
#     # # Specifically when using .values() to get specific columns, or .values_list() [function unknown yet], the query returns....
#     #     #    !!!  DICTIONARY  !!!
#     # for e in exercises:
#     #     # print(e.keys())
#         # print(f"{e["trainer__name"]}, recommends {e["name"]}, with a default rep count of {e["default_reps"]}")
        
    
#     # # [ Filtering & Comparison (__) ]
#     # # 5 - Exact- / Case-Insenstive Matches
#     # # 6 - Partial Matches
#     # trainers = Trainer.objects.filter(name__exact="Sarah Chen")     # Exact Match
#     trainers = Trainer.objects.all()
#     print(trainers)
#     for trainer in trainers:
#         print(trainer)
#         print(trainer.name)
#         print("---")
#     # trainers = Trainer.objects.filter(name__contains="A")   # Case Sensitive
#     # trainers = Trainer.objects.filter(name__icontains="t")  # Case Insensitive
#     # trainers = Trainer.objects.filter(email__startswith="alex")     # Starts-with Case Sens
#     # trainers = Trainer.objects.filter(email__istartswith="jordan")  # Starts-wtih Cases Insens
#     # trainers = Trainer.objects.filter(email__endswith="...")    # You get the picture

#     # # 7 - Numeric Comparisons
#     # exercises = Exercise.objects.filter(default_sets__gt=3)
#     # exercises = Exercise.objects.filter(default_reps__gte=10)
#     # exercises = Exercise.objects.filter(default_weights__lt=100)
#     # exercises = Exercise.objects.filter(default_reps__lte=8)

#     # for e in exercises:
#     #     # print(f"{e.name}: Default sets: {e.default_sets}")
#     #     print(f"{e.name}: Default sets: {e.default_reps}")
#     #     # print(f"{e.name}: Default sets: {e.default_weights}")

#     # 8 - Membership Checks


#     # [ Relational Queries (Joins Spanning Tables) ]
#     # # 9 - Forward Lookup (Filter something by a column in another table linked to it)
#     # workout_exercises = WorkoutExercise.objects.all()
#     # for we in workout_exercises:
#     #     print(f"{we.exercise.name} - {we.workout.client_remarks or "N/A"}")


#     # 10 - Reverse Lookup (Filter with a table that has no direct FK relation;  Django should be able to trace it regardless)
#     #   !!!! THIS IS WHERE WE USE THE related_name !!!!!!!!!!!!!
#         # This is how Django handles looking up tables in the reverse direction despite there being NO EXPLICIT FK

#     # # "clients" table has no FK to "workouts", but "workouts" has a FK to "clients"
#     # # "exercises" table has no FK to "workout_exercises", but "workout_exercises" has a FK to "exercises"
#     #     #      !!! Django uses the    --> related_name <--     param defined for FK columns to facilitate reverse lookups
#     # clients = Client.objects.filter(workouts__exercise_workout_exercise__default_reps__gt=5)
#     # for c in clients:
#     #     print(f"{c.name} did ")

#     # # "exercises" table has no FK to "tags_exercises", but "tags_exercises" has FK to "exercises",
#     # # ... with a related_name of "exercises_tags"
#     # exercises = Exercise.objects.filter(exercises_tags__tag_id=5)
#     # for e in exercises:
#     #     print(f"{e.name}")

#     #     # print(f"{e.name} has a tag named {e.exercises_tags.name} that has an ID of {e.exercises_tags.tag_id}")
#     #     # ^ This will   !!! NOT WORK !!!
#     #     # If we want to ACCESS THE COLUMNS from the QuerySet THROUGH A REVERSE LOOKUP, we need to use the following syntax:
#     # for e in exercises:
#     #     for rel in e.exercises_tags.all():   # iterate the junction rows
#     #         print(f"{e.name} has tag_id {rel.tag_id}")
#     #     # I also don't know the syntax or logic, but future-me problem for the time being

#     # # 11 - Deep Relationship Spanning (Filter something across a junction table, so 3 table spanning filter)
#     # workout_exercises = WorkoutExercise.objects.filter(workout__client__id__gte=4)
#     # workout_exercises = WorkoutExercise.objects.filter(workout__client__id__gte=4, workout__client__name__icontains="L")
#     # for we in workout_exercises:
#     #     print(f"{we.id} - {we.workout.client.name}({we.workout.client.id}) - {we.exercise.name}")

#     # # 12 - One-to-One Filtering
#     # client_info = ClientInfo.objects.filter(client__name__startswith="J")
#     # for ci in client_info:
#     #     print(f"{ci.client.name} : {ci.client.email}")  # Use DOT here, NOT Underscore,
#     #                                                     # we're no longer dealing with models, just treat as nested object

    
#     # [ Ordering & Aggregation ]
#     # # 13 - Ordering
#     # tags = Tag.objects.order_by('-id')
#     # for t in tags:
#     #     print(f"{t.id}: {t.name}")


#     # # 14 - Counting
#     # trainer_client_count = Client.objects.filter(trainer__name__exact="Alex Rivera").count()
#     # #   !!!!! USE related_name HERE FOR REVERSE LOOKUP AGAIN !!!!!!!
#     # trainer_client_count = Trainer.objects.filter(clients__trainer__name__exact="Alex Rivera").count()
#     # print(f"{trainer_client_count}")

#     # # 15 - Mathematical Aggregates
#     # # This needs (at the very top) `from django.db.models import Avg`
#     # # aggregate() also produces a   !!! DICTIONARY !!!
#     # avg_workout_exercise_reps = WorkoutExercise.objects.aggregate(avg_reps=Avg('reps'))
#     # print(f"Average workout_exercise reps across workouts: {avg_workout_exercise_reps['avg_reps']}")



#     return render(request, "trainer/query.html", {})