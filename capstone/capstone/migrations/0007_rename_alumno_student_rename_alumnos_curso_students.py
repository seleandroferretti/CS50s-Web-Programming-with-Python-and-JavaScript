# Generated by Django 4.2.5 on 2023-10-08 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0006_rename_profesor_teacher_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Alumno',
            new_name='Student',
        ),
        migrations.RenameField(
            model_name='curso',
            old_name='alumnos',
            new_name='students',
        ),
    ]
