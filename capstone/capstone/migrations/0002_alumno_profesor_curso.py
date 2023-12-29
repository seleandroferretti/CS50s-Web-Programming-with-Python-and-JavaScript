# Generated by Django 4.2.5 on 2023-10-04 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('documento', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('documento', models.TextField(max_length=255)),
                ('profesion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('categoria', models.TextField(choices=[('1', 'Programacion'), ('2', 'Marketing'), ('3', 'Producto'), ('4', 'Datos'), ('5', 'Ciberseguridad'), ('6', 'Finanzas')])),
                ('fecha_inicio', models.TextField(max_length=255)),
                ('fecha_fin', models.TextField(max_length=255)),
                ('temario', models.TextField(max_length=5000)),
                ('alumnos', models.ManyToManyField(to='capstone.alumno')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capstone.profesor')),
            ],
        ),
    ]
