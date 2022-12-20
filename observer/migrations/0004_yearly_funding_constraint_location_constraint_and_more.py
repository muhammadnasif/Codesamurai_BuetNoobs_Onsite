# Generated by Django 4.1.4 on 2022-12-20 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0003_component_budget_ratio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yearly_Funding_Constraint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_funding', models.IntegerField()),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observer.agency')),
            ],
        ),
        migrations.CreateModel(
            name='Location_Constraint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_limit', models.IntegerField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observer.location')),
            ],
        ),
        migrations.CreateModel(
            name='Agency_Constraint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_limit', models.IntegerField()),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='observer.agency')),
            ],
        ),
    ]