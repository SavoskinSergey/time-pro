# Generated by Django 4.2 on 2023-07-18 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_project', '0006_project_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='author',
        ),
    ]