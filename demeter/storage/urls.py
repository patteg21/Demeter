from django.urls import path
from . import views


urlpatterns = [
    path("",views.dashers, name="dashers"),
]