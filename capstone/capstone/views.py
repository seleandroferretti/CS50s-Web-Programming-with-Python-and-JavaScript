from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from .models import User, Curso, Student, Teacher
import json

def index(request):
    cursos = Curso.objects.all().order_by('id')
    paginator = Paginator(cursos, 5)
    page_number = request.GET.get('page')
    cursos_per_page = paginator.get_page(page_number)
    
    categorias = Curso.Categoria.choices
    opciones_categorias = [{'valor': valor, 'nombre': nombre} for valor, nombre in categorias]

    teachers = Teacher.objects.all()
    
    return render(request, "capstone/index.html", {"cursos_per_page" : cursos_per_page, "categorias": opciones_categorias, "teachers": teachers})

def view_course(request, pk):
    course = Curso.objects.get(pk=pk)
    students = course.students.all()
    return render(request, "capstone/view_course.html", {"course": course, "students" : students})

@login_required
def students_management(request, pk):
    course = Curso.objects.get(pk=pk)
    all_students = Student.objects.all()
    enrolled_students = course.students.all()
    available_students = all_students.exclude(pk__in=[student.pk for student in enrolled_students])
    return render(request, "capstone/modal.html", {"available_students": available_students, "enrolled_students": enrolled_students, "course": course})

@login_required
@csrf_exempt
def save_enrolled_students(request, pk):
    course = Curso.objects.get(pk=pk)
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        students = data.get('students', [])

        existing_student_ids = course.students.values_list('id', flat=True)

        new_students = [student for student in students if int(student['id']) not in existing_student_ids]

        for student in new_students:
            student_object = Student.objects.get(id=int(student['id']))
            course.students.add(student_object)

        students_to_remove = Student.objects.filter(id__in=existing_student_ids).exclude(id__in=[int(student['id']) for student in students])
        course.students.remove(*students_to_remove)

        return JsonResponse({'message': 'Cambios guardados con éxito'})

    return JsonResponse({'message': 'Método no permitido'}, status=405)

@login_required
def students(request):
    students = Student.objects.all().order_by('id')
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    students_per_page = paginator.get_page(page_number)
    return render(request, "capstone/students.html", {"students_per_page" : students_per_page})

@login_required
def teachers(request):
    teachers = Teacher.objects.all().order_by('id')
    paginator = Paginator(teachers, 5)
    page_number = request.GET.get('page')
    teachers_per_page = paginator.get_page(page_number)
    return render(request, "capstone/teachers.html", {"teachers_per_page" : teachers_per_page})

@login_required
def new_student(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        documento = request.POST["documento"]

        student = Student.objects.create(
            nombre=nombre,
            documento=documento
        )
        return redirect("students")
    return render(request, "capstone/new_student.html")

@login_required
def new_teacher(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        documento = request.POST["documento"]
        profesion = request.POST["profesion"]

        teacher = Teacher.objects.create(
            nombre=nombre,
            documento=documento,
            profesion=profesion
        )
        return redirect("teachers")
    return render(request, "capstone/new_teacher.html")

@login_required
def new_course(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        categoria = request.POST["categoria"]
        fecha_inicio = request.POST["fecha_inicio"]
        fecha_fin = request.POST["fecha_fin"]
        temario = request.POST["temario"]
        teacher_id = request.POST["teacher_id"]
        teacher = Teacher.objects.get(id=teacher_id)

        curso = Curso.objects.create(
            nombre=nombre,
            categoria=categoria,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            temario=temario,
            teacher=teacher
        )
        return redirect("index")
    return render(request, "capstone/new_course.html", {"categorias" : Curso.Categoria.choices, "teachers" : Teacher.objects.all()})

@login_required
@csrf_exempt
def save_changes_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        estudiante_id = data.get('estudianteId')
        nuevo_nombre = data.get('nombre')
        nuevo_documento = data.get('documento')

        estudiante = get_object_or_404(Student, id=estudiante_id)
        estudiante.nombre = nuevo_nombre
        estudiante.documento = nuevo_documento
        estudiante.save()

        return JsonResponse({'message': 'Cambios guardados correctamente.'})
    else:
        return JsonResponse({'message': 'Método de solicitud no válido.'}, status=400)

@login_required
@csrf_exempt
def save_changes_teacher(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher_id = data.get('teacherId')
        nuevo_nombre = data.get('nombre')
        nuevo_documento = data.get('documento')
        nueva_profesion = data.get('profesion')

        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher.nombre = nuevo_nombre
        teacher.documento = nuevo_documento
        teacher.profesion = nueva_profesion
        teacher.save()

        return JsonResponse({'message': 'Cambios guardados correctamente.'})
    else:
        return JsonResponse({'message': 'Método de solicitud no válido.'}, status=400)

@login_required
@csrf_exempt
def save_changes_course(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        course_id = data.get('courseId')
        nuevo_nombre = data.get('nombre')
        nueva_categoria = data.get('categoria')
        nueva_fecha_inicio = data.get('fecha_inicio')
        nueva_fecha_fin = data.get('fecha_fin')
        nuevo_temario = data.get('temario')
        nuevo_teacher = data.get('teacher')

        course = get_object_or_404(Curso, id=course_id)
        course.nombre = nuevo_nombre
        course.categoria = nueva_categoria
        course.fecha_inicio = nueva_fecha_inicio
        course.fecha_fin = nueva_fecha_fin
        course.temario = nuevo_temario
        course.teacher_id = nuevo_teacher
        course.save()

        return JsonResponse({'message': 'Cambios guardados correctamente.'})
    else:
        return JsonResponse({'message': 'Método de solicitud no válido.'}, status=400)

@login_required
def generate_pdf(request, pk):
    course = get_object_or_404(Curso, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{course.nombre}.pdf"'

    p = canvas.Canvas(response)
    p.setTitle(f'{course.nombre}')
    p.setFont('Helvetica-Bold', 18)
    p.drawString(200, 770, f'{course.nombre}')

    categoria_text = 'Category: '
    categoria_value = next((nombre for id, nombre in Curso.Categoria.choices if id == course.categoria), None)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(100, 740, categoria_text)
    p.setFont('Helvetica', 12)
    p.drawString(165, 740, categoria_value)

    fecha_inicio_text = 'Start Date: '
    fecha_fin_text = 'End Date: '

    p.setFont('Helvetica-Bold', 12)
    p.drawString(100, 720, fecha_inicio_text)
    p.setFont('Helvetica', 12)
    p.drawString(165, 720, f'{course.fecha_inicio}')

    p.setFont('Helvetica-Bold', 12)
    p.drawString(100, 700, fecha_fin_text)
    p.setFont('Helvetica', 12)
    p.drawString(165, 700, f'{course.fecha_fin}')

    p.setFont('Helvetica-Bold', 12)
    p.drawString(100, 680, f'Programme PDF link:')
    p.setFont('Helvetica', 10)
    p.drawString(120, 660, f'{course.temario}')  

    teacher_name = course.teacher.nombre
    teacher_text = 'Teacher: '

    p.setFont('Helvetica-Bold', 12)
    p.drawString(100, 640, teacher_text)
    
    p.setFont('Helvetica', 12)
    p.drawString(160, 640, teacher_name)

    p.setFont('Helvetica-Bold', 12)
    p.drawString(100, 620, f'Enrolled Students:')

    students = course.students.all()

    for i, student in enumerate(students):
        p.setFont('Helvetica', 12)
        p.drawString(120, 600 - i*25, f'{student.nombre}')

    p.showPage()
    p.save()

    return response

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")
