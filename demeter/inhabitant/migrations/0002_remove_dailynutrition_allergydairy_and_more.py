# Generated by Django 4.2.3 on 2023-08-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inhabitant", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dailynutrition",
            name="allergyDairy",
        ),
        migrations.RemoveField(
            model_name="dailynutrition",
            name="allergyGluten",
        ),
        migrations.RemoveField(
            model_name="dailynutrition",
            name="isVegetarian",
        ),
        migrations.AddField(
            model_name="inhabitant",
            name="allergyDairy",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="inhabitant",
            name="allergyGluten",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="inhabitant",
            name="isVegetarian",
            field=models.BooleanField(default=False),
        ),
    ]
