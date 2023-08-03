from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("monitor",views.healthMonitor,name="monitor"),
    path("interface", views.interface ,name="interface"),
    path("movement", views.movement, name="movement"),
    path("order", views.orderItems, name="order"),
    path("monitor/<str:inhabitantID>", views.joinInhabDash, name="inhabdash"),
]