# Generated by Django 4.1.4 on 2022-12-20 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0009_alter_project_core_project_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposed_project',
            name='proposed_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
