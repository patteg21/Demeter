# Generated by Django 4.2.3 on 2023-08-05 13:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0003_dasher_rationheld"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="livingfacility",
            name="heightZ",
        ),
        migrations.RemoveField(
            model_name="livingfacility",
            name="lengthX",
        ),
        migrations.RemoveField(
            model_name="livingfacility",
            name="lengthY",
        ),
        migrations.RemoveField(
            model_name="storagefacility",
            name="heightZ",
        ),
        migrations.RemoveField(
            model_name="storagefacility",
            name="lengthX",
        ),
        migrations.RemoveField(
            model_name="storagefacility",
            name="lengthY",
        ),
        migrations.AddField(
            model_name="dasher",
            name="locationX",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="dasher",
            name="locationY",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="livingfacility",
            name="locationX",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="livingfacility",
            name="locationY",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="storagefacility",
            name="locationX",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="storagefacility",
            name="locationY",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="dasher",
            name="status",
            field=models.CharField(
                choices=[
                    ("Stopped", "Stopped"),
                    ("In-Progress", "In-Progress"),
                    ("Destination", "Destination"),
                ],
                default="Stopped",
                max_length=64,
            ),
        ),
    ]
