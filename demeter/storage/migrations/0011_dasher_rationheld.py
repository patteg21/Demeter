# Generated by Django 4.2.3 on 2023-08-05 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("container", "0003_alter_typeration_rationid"),
        ("storage", "0010_remove_dasher_rationheld"),
    ]

    operations = [
        migrations.AddField(
            model_name="dasher",
            name="rationHeld",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="container.typeration",
            ),
        ),
    ]
