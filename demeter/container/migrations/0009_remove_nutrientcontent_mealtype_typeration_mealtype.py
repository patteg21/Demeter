# Generated by Django 4.2.3 on 2023-08-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("container", "0008_nutrientcontent_mealtype"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nutrientcontent",
            name="mealType",
        ),
        migrations.AddField(
            model_name="typeration",
            name="mealType",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Breakfast", "Breakfast"),
                    ("Lunch", "Lunch"),
                    ("Dinner", "Dinner"),
                    ("Snack", "Snack"),
                    ("Any", "Any"),
                ],
                default="Storage",
                max_length=64,
                null=True,
            ),
        ),
    ]
