# Generated by Django 4.1.4 on 2022-12-20 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0005_remove_user_usertype_user_agency_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_core',
            name='location',
        ),
        migrations.AddField(
            model_name='project_core',
            name='locations',
            field=models.ManyToManyField(to='observer.location'),
        ),
    ]
