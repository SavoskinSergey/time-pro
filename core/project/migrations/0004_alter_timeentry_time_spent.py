# Generated by Django 4.2 on 2023-04-14 20:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_project', '0003_timeentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeentry',
            name='time_spent',
            field=models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(0)]),
        ),
    ]
