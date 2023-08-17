from django.shortcuts import render
from .forms import *
from .models import *
from inhabitant.models import *

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = ContainerForm()
        return render(request, "container/container_form.html",{
            "form": form,
            "test": "test",
        })

