from django.db import models
from container.models import *
from inhabitant.models import *

# Create your models here.


class StorageFacility(models.Model):

    # Primary Key
    storageFacilityID = models.AutoField(primary_key=True,)

    # Dimesions of the Storage Facility
    lengthX = models.IntegerField(default=100) # Feet
    lengthY = models.IntegerField(default=100) # Feet
    heightZ = models.IntegerField(default=100) # Feet


    def __str__(self):
        return f"Storage Facility {self.storageFacilityID}"

class LivingFacility(models.Model):

    # Primary Key
    livingFacilityID = models.AutoField(primary_key=True)

    # Dimesions of the Living Facility
    lengthX = models.IntegerField(default=100) # Feet
    lengthY = models.IntegerField(default=100) # Feet
    heightZ = models.IntegerField(default=100) # Feet



    def __str__(self):
        return f"Living Facility {self.livingFacilityID}"

class Transit(models.Model):
    location = "In Transit"


class Mover(models.Model):

    # Mover's stay within a specific storage unit
    locationMover = models.ForeignKey(StorageFacility, on_delete=models.PROTECT)

    # container being held/moved
    containerHeld = models.ForeignKey(Container, on_delete=models.PROTECT, null=True)

    # Primary Key
    moverID = models.AutoField(primary_key=True)

    # Status as to whether the mover is moving something/in motion
    STATUS= [
        ("Stopped","Stopped"),
        ("In-progress","In-progress"),
    ]
    status = models.CharField(max_length=64,default="Stopped",choices=STATUS)



class Dasher(models.Model):
    # Foreign Keys
    

    # Primary Key
    dasherID = models.AutoField(primary_key=True)

    # Whether the dasher is moving or is stationary
    STATUS= [
        ("Stopped","Stopped"),
        ("In-Progress","In-Progress"),
    ]
    status = models.CharField(max_length=64,default="Stopped",choices=STATUS)