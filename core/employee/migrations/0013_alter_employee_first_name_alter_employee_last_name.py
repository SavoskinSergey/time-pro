# Generated by Django 4.2 on 2023-08-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_employee', '0012_alter_department_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]