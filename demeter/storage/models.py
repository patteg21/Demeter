from django.db import models
from container.models import *
from inhabitant.models import *

# Create your models here.



class Mover(models.Model):

    # Mover's stay within a specific storage unit
    locationMover = models.ForeignKey(Facility, on_delete=models.PROTECT)

    # container being held/moved
    containerHeld = models.ForeignKey(Container, default=None, on_delete=models.PROTECT, null=True, related_name="Mover")

    # Primary Key
    moverID = models.AutoField(primary_key=True)

    # Status as to whether the mover is moving something/in motion
    STATUS= [
        ("Stopped","Stopped"),
        ("In-progress","In-progress"),
    ]
    status = models.CharField(max_length=64,default="Stopped",choices=STATUS)

    def __str__(self):
        return f"Mover {self.moverID}"


class Dasher(models.Model):

    # holds a single ration of a certain type. tbd
    rationHeld = models.ForeignKey(TypeRation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    #Location
    locationX = models.IntegerField(default=0)
    locationY = models.IntegerField(default=0)

    # Associates a location with location
    location = models.ForeignKey(Facility,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # Primary Key
    dasherID = models.AutoField(primary_key=True)

    # Whether the dasher is moving or is stationary
    
    STATUS= [
        ("Stopped","Stopped"),
        ("In-Progress","In-Progress"),
    ]
    status = models.CharField(max_length=64,default="Stopped",choices=STATUS)

    def __str__(self):
        
        if self.rationHeld == None:
            return f"Dasher {self.dasherID}"

        return f"Dasher {self.dasherID}"