# Generated by Django 4.2 on 2023-07-12 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_task', '0004_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='charge',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=10),
        ),
    ]
