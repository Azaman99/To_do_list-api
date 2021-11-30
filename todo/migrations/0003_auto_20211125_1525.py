# Generated by Django 3.2.9 on 2021-11-25 14:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20211125_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='task',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]