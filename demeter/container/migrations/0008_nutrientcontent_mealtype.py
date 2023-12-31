# Generated by Django 4.2.3 on 2023-08-22 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("container", "0007_alter_container_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="nutrientcontent",
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
