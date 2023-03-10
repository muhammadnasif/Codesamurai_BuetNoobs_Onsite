# Generated by Django 4.1.4 on 2022-12-21 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0013_alter_usertypes_code_alter_usertypes_committee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='budget_used',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='approved_project',
            name='actual_cost',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='project_core',
            name='expected_cost',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='yearly_funding_constraint',
            name='max_funding',
            field=models.BigIntegerField(),
        ),
    ]
