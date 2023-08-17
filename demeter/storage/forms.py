from django import forms
from container.models import *
from .models import *
from inhabitant.models import *

# Define forms below

class DasherMoveForm(forms.ModelForm):
    class Meta:
        model = Dasher
        # fields = "__all__"
        fields = [
            "location"
            ]  


# allows you to choose a specifc facility    
class FacilityForm(forms.Form):
    facility = forms.ModelChoiceField(queryset=Facility.objects.all())