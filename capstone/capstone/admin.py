from django.contrib import admin

# Register your models here.
from capstone.models import User, Teacher, Student, Curso

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Curso)