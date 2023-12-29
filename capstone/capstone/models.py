from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Teacher(models.Model):
    nombre = models.CharField(max_length=255)
    documento = models.TextField(max_length=255)
    profesion = models.CharField(max_length=255)

class Student(models.Model):
    nombre = models.CharField(max_length=255)
    documento = models.TextField(max_length=255)

class Curso(models.Model):
    class Categoria(models.TextChoices):
        PROGRAMMING = '1','Programming'
        MARKETING = '2','Marketing'
        PRODUCT = '3','Product'
        DATA = '4','Data'
        CYBERSECURITY = '5','Cybersecurity'
        FINANCE = '6','Finance'

    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    fecha_inicio = models.TextField(max_length=255)
    fecha_fin = models.TextField(max_length=255)
    temario = models.TextField(max_length=5000)
