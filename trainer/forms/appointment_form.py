from django import forms
from django.contrib.auth import get_user_model

from orm.models import Appointment, Client

UserTrainer = get_user_model()    

class AppointmentForm(forms.ModelForm):

    client = forms.ModelChoiceField(
        queryset = Client.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    scheduled_time = forms.ChoiceField(
        choices = Appointment.PREFERRED_TIMES,
        widget = forms.Select(attrs={"class":"form-control"})
    )

    class Meta:
        model = Appointment
        fields = ["client", "scheduled_date", "scheduled_time"]
        labels = {
            "client": "Client",
            "scheduled_date": "Scheduled Date",
            "scheduled_time": "Scheduled Time"
        }
        widgets = {
            "scheduled_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "scheduled_time": forms.TextInput(attrs={"class": "form-control"}),
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
            # this will create a list of clients when used in the template
            self.fields['client'].queryset = Client.objects.filter(trainer=userTrainer)