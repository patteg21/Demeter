from django.db import models
from django.core.validators import MaxValueValidator,MinLengthValidator


# Create your models here.
class Facility(models.Model):

    # Primary Key
    facilityID = models.AutoField(primary_key=True,)

    # location field for Dasher to reference
    locationX = models.IntegerField(default=0)
    locationY = models.IntegerField(default=0)

    #Type of Facility options
    FACILITIES = [
        ("Storage","Storage"),
        ("Living","Living"),
        ("Sorting Area","Sorting Area"),
        ("Other","Other"),
    ]
 
    typeFacility = models.CharField(
        max_length=64,
        default="Storage",
        choices=FACILITIES,
        null=False,
        blank=False,
        )

    def __str__(self):
        return f"Facility {self.facilityID} - {self.typeFacility}"


class Container(models.Model):
    containerID = models.AutoField(primary_key=True, blank=False)

    rationPacks = models.IntegerField(default=1, blank=False)

    sensorContainer = models.CharField(max_length=64, null=True, blank=True)

    location = models.ForeignKey(Facility,
    on_delete=models.PROTECT,
    blank=False,
    )


    def __str__(self) -> str:
        return f"Container: {self.containerID}"



class TypeRation(models.Model):
    rationID = models.AutoField(primary_key=True, blank=False)
    rationImg = models.ImageField(default=None, blank=True)
    rationType = models.CharField(max_length=64, default=None)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.rationType}"



class RationPack(models.Model):
    rationPackID = models.CharField(max_length=64,primary_key=True)
     
    #                       --> FOREIGN KEYS
    typeRation = models.ForeignKey(TypeRation,
        default=None,
        on_delete=models.PROTECT,
        related_name="RationPack",
    )

    container = models.ForeignKey(Container,
        default=None, 
        on_delete=models.CASCADE,
        related_name="RationPack")
    
    # the capacity of rations within a ration pack
    rations = models.IntegerField(default=1)
    
    # need to determine how the sensor works and how it gets information
    sensorRationPack = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):

        if self.rations <= 0:
            return f"Ration Pack - Empty"

        return f"Ration Pack - {self.typeRation}"



class NutrientContent(models.Model):
     #                       --> FOREIGN KEYS
    ration = models.ForeignKey(TypeRation, 
        default=None, 
        blank=False,
        on_delete=models.PROTECT,
        related_name="NutrientContent")
 

    calories = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    fiber = models.IntegerField()
    protein = models.IntegerField()

    #Defaults are set to it so that allergies and intolerances are assumed
    isPlantBased = models.BooleanField(default=False)
    isOrganic = models.BooleanField(default=False)
    containtsGluten = models.BooleanField(default=True)
    containtsDairy = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.ration}"


class Sensor(models.Model):
    sensorID = models.CharField(max_length=64,primary_key=True)
    coordinateX = models.IntegerField()
    coordinateY = models.IntegerField()
    coordinateZ = models.IntegerField()
    status = models.CharField(max_length=64)
    temperature = models.IntegerField()

