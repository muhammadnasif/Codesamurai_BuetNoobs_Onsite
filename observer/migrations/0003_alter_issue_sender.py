# Generated by Django 4.1.4 on 2022-12-19 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='sender',
            field=models.CharField(default='Nasif', max_length=200),
        ),
    ]
