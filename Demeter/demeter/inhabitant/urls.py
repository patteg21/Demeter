from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("health",views.healthMonitor,name="health"),
    path("interface", views.interface ,name="interface"),
    path("movement", views.movement, name="movement"),
    path("order", views.orderItems, name="order"),
    path("health/<str:id>", views.joinInhabDash, name="indabitantDashboard"),
]