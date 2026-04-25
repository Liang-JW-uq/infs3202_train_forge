from django import forms
from orm.models import Tag
from django.core.validators import MinLengthValidator

class TagForm(forms.ModelForm):

    # Another option
    # name = forms.CharField(
    #     label="tag name",
    #     # widget - more for 'formatting' the gerrate html element
    #     widget=forms.TextInput(attrs={ "class": "form-control" })
    # )

    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Tag Name'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        validation = {
            'name': [MinLengthValidator(5)]
        }