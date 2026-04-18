from django import forms
from orm.models import Workout, WorkoutExercise
from django.core.validators import MinLengthValidator
from django.forms import inlineformset_factory

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['client', 'is_completed', 'trainer_review', 'client_remarks', 'ai_feedback']


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'is_done', 'pre_sets', 'pre_reps', 'pre_weight', 'pre_duration']


# This is to allow nested WorkoutExercise Forms underneath each Workout as an "Inline Formset"
WorkoutExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    form=WorkoutExerciseForm,
    extra=0,
    can_delete=True
) 