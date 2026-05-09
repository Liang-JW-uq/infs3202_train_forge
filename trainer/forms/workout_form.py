from django import forms
from orm.models import Workout, WorkoutExercise, Client
from django.core.validators import MinLengthValidator
from django.forms import inlineformset_factory

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['client', 'is_completed', 'trainer_review', 'client_remarks', 'ai_feedback']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'form-control',
                'hx-get': '/client/info',
                'hx-trigger': 'change',
                'hx-target': '#client-info'
            }),
            'trainer_review': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'client_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ai_feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'style': 'display: none'}),
        }
        labels = {
            'client': 'Select a client:'
        }
    
    def __init__(self, *args, **kwargs):
        # **kwargs = {'instance': instance, 'trainer': trainer'} from the views for edit/add

        # have to remote this trainer from **kwargs
        # we use this trainer to filter exercises for this trainer only (Saas)
        userTrainer = kwargs.pop("userTrainer", None)
        # when calling superclass/parent, **kwargs can be only one item
        # we have remove the trainer from **kwargs using pop above
        super().__init__(*args, **kwargs)

        if userTrainer:
            # this will create a list of tags when used in the template
            self.fields['client'].queryset = Client.objects.filter(trainer=userTrainer)


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'is_done', 'pre_sets', 'pre_reps', 'pre_weight', 'pre_duration',
                  'actual_sets', 'actual_reps', 'actual_weight', 'actual_duration']
        widgets = {
            'exercise': forms.Select(attrs={'style': 'pointer-events:none;'}),
            'pre_sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'pre_reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'pre_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'pre_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_duration': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # all the prescribe exercise values are to be marked non editable
        if self.instance and self.instance.pk:
            readonly_fields = ['pre_sets', 'pre_reps', 'pre_weight', 'pre_duration']
            
            for field_name in readonly_fields:
                if field_name in self.fields:
                    self.fields[field_name].disabled = True
                    self.fields[field_name].widget.attrs['readonly'] = True
                    self.fields[field_name].required = False
                    self.fields[field_name].widget.attrs['class'] = 'form-control'







# This is to allow nested WorkoutExercise Forms underneath each Workout as an "Inline Formset"
WorkoutExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    form=WorkoutExerciseForm,
    extra=0,
    can_delete=True
) 