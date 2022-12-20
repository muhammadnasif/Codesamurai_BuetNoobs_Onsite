# Generated by Django 4.1.4 on 2022-12-20 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("observer", "0006_remove_project_core_location_project_core_locations"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("feedback", models.CharField(max_length=200)),
                (
                    "project_core",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="observer.project_core",
                    ),
                ),
            ],
        ),
    ]
