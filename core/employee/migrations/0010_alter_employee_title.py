# Generated by Django 4.2 on 2023-04-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_employee', '0009_alter_employee_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]