# Generated by Django 4.2 on 2023-04-12 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_employee', '0006_employee_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='department',
            new_name='department_name',
        ),
    ]