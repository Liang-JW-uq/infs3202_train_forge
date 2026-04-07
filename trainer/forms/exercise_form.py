from django import forms
from orm.models import Exercise, Tag
from django.core.validators import MinLengthValidator, MinValueValidator

class ExerciseForm(forms.ModelForm):

    # Multiple-Choice is a bit finnicky with Bootstrap;
    # Need to define a queryset, to list down all the choices
    # Here we MUST put none(), otherwise ALL tags from ALL trainers will be included
    # Later we will pass back the appropriate Trainer object, and ONLY its own Tags, ** FROM THE VIEW ADD/EDIT**
    tags = forms.ModelMultipleChoiceField(
        # queryset = Tag.objects.all(),
        queryset=Tag.objects.none(),        # Must start with none, or we take EVERYTHING from other trainers as well
        widget=forms.CheckboxSelectMultiple(attrs={"class": "btn-check"}) # Mandatory Bootstrap Styling for multi-checkbox select
    )

    class Meta:
        model = Exercise
        fields = ['name', 'instructions', 'def_sets', 'def_reps', 'def_weight', 'def_duration', 'tags']
        label = {
            'name': "Exercise Name",
            'instructions': "Instructions",
            "tags": "Tags",
            'def_sets': "Sets (Default)",
            'def_reps': "Reps (Default)",
            'def_weight': "Weight (kg) (Default)",
            'def_duration': "Duration (Minutes) (Default)"
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'def_sets': forms.NumberInput(attrs={'class': 'form-control', "value": 99}),
            'def_reps': forms.NumberInput(attrs={'class': 'form-control', "value": 0}),
            'def_weight': forms.NumberInput(attrs={'class': 'form-control', "value": 0}),
            'def_duration': forms.NumberInput(attrs={'class': 'form-control', "value": 0})
        }
        validation = {
            'def_sets': [MinValueValidator(0)],
            'def_reps': [MinValueValidator(0)],
            'def_weight': [MinValueValidator(0)],
            'def_duration': [MinValueValidator(0)],
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
            self.fields['tags'].queryset = Tag.objects.filter(trainer=userTrainer)