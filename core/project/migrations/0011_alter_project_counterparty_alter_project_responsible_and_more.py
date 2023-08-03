# Generated by Django 4.2 on 2023-08-03 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_employee', '0012_alter_department_account'),
        ('core_project', '0010_alter_project_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='counterparty',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='responsible',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core_employee.employee'),
        ),
        migrations.AlterField(
            model_name='project',
            name='stage',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
