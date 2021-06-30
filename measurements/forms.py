from django import forms
from django.forms.models import ModelForm
from .models import Measurement

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('destination',)

        widgets = {
            'destination': forms.TextInput(attrs = {'placeholder': 'Enter your destination'}),
        }