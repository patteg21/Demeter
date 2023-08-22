# Generated by Django 4.2.3 on 2023-08-22 19:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("container", "0010_alter_typeration_mealtype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="typeration",
            name="mealType",
            field=models.CharField(
                choices=[
                    ("Breakfast", "Breakfast"),
                    ("Lunch", "Lunch"),
                    ("Dinner", "Dinner"),
                    ("Snack", "Snack"),
                ],
                default="Storage",
                max_length=64,
            ),
        ),
    ]
