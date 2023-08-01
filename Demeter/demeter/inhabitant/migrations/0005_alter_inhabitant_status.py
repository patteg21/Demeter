# Generated by Django 4.2.3 on 2023-07-31 18:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inhabitant", "0004_alter_dailynutrition_datenutrition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inhabitant",
            name="status",
            field=models.CharField(
                choices=[
                    ("Healthy", "Healthy"),
                    ("Sick", "Sick"),
                    ("Recovering", "Recovering"),
                    ("Injured", "Injured"),
                    ("Deceased", "Deceased"),
                ],
                default="Healthy",
                max_length=64,
            ),
        ),
    ]
