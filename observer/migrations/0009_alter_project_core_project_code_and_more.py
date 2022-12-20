# Generated by Django 4.1.4 on 2022-12-20 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0008_remove_approved_project_completion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_core',
            name='project_code',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='proposed_project',
            name='proposed_date',
            field=models.DateField(auto_now=True),
        ),
    ]
