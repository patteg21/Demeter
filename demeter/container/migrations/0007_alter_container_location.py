# Generated by Django 4.2.3 on 2023-08-09 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("container", "0006_alter_facility_typefacility"),
    ]

    operations = [
        migrations.AlterField(
            model_name="container",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="container.facility"
            ),
        ),
    ]
