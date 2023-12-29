
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_course", views.new_course, name="new_course"),
    path("teachers", views.teachers, name="teachers"),
    path("students", views.students, name="students"),
    path("new_teacher", views.new_teacher, name="new_teacher"),
    path("new_student", views.new_student, name="new_student"),
    path("course/<int:pk>/", views.view_course, name="view_course"),
    path("course/<int:pk>/students_management/", views.students_management, name="students_management"),
    path("course/<int:pk>/save_enrolled_students/", views.save_enrolled_students, name="save_enrolled_students"),
    path('course/<int:pk>/generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('save_changes_student/', views.save_changes_student, name='save_changes_student'),
    path('save_changes_teacher/', views.save_changes_teacher, name='save_changes_teacher'),
    path('save_changes_course/', views.save_changes_course, name='save_changes_course')
]
