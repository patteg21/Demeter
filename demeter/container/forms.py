from django import forms
from .models import *

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ['rationPacks','sensorContainer']
