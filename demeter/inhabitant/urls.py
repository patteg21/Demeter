from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("monitor/",views.healthMonitor,name="monitor"),
    path("interface/", views.interface ,name="interface"),
    path("containers/", views.containers, name="containers"),
    path("monitor/<str:inhabitantID>/", views.joinInhabDash, name="inhabdash"),
    path("facilities/", views.facilities, name="facilities"),
    path("facilities/<str:facilityID>/", views.joinFacilityDash,name="facilitydash")
]