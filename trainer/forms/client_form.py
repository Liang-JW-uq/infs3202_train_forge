from django import forms
from orm.models import Client

class ClientForm(forms.ModelForm):

    # Widget specifically refers to HTML classes & properties
    # Everything else will (mostly) be Django model-related syntax

    goals = forms.CharField(
        label="myGoals",
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Type your fitness goals here", "rows": 3})
    )
    class Meta:
        model = Client
        fields = ["name", "age", "email", "contact_no", "goals"]
        # labels = {
        #     "name": "nama"
        # }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Type your name here"})
        }


# class Meta:
#     model = Workout
#     fields = ['trainer', 'client', 'scheduled_date', 'is_completed', 'trainer_review', 'client_remarks']
#     widgets = {
#         'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
#         'trainer': forms.Select(attrs={'class': 'form-control'}),
#         'client': forms.Select(attrs={'class': 'form-control'}),
#         # 'trainer_review': forms.Textarea(attrs={'class': 'form-control'}),
#         # 'client_remarks': forms.Textarea(attrs={'class': 'form-control'}),
#     }