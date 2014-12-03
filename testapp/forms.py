from django import forms
from testapp.models import Greeting

class CreateGreetingForm(forms.ModelForm):
    class Meta:
        model = Greeting
        exclude = ['author', 'date']