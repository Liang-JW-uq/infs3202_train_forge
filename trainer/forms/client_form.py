from django import forms
from orm.models import Client

class ClientForm(forms.ModelForm):

    # Widget specifically refers to HTML classes & properties
    # Everything else will (mostly) be Django model-related syntax

    goals = forms.CharField(
        label="Goals",
        strip=True,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Type your fitness goals here", "rows": 3})
    )
    preferred_times = forms.ChoiceField(
        choices = Client.PREFERRED_TIMES,
        widget = forms.Select(attrs={"class":"form-control"})
    )
    class Meta:
        model = Client
        fields = ["name", "age", "email", "contact_no", "goals", "height", "weight", "preferred_times"]
        labels = {
            "name": "Name",
            "email": "Email",
            "age": "Age",
            "contact_no": "Contact No.",
            "height": "Height (m)",
            "weight": "Weight (kg)",
            "goals": "Goals",
            "preferred_times": "Preferred Times"
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your name here"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email here"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter your age here"}),
            "contact_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your contact no. here"}),
            "height": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter your height here"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter your weight here"}),
        }
        