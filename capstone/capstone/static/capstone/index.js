document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('myModal');
    var openModalButton = document.getElementById('openModalButton');

    openModalButton.addEventListener('click', function() {
        const id = this.value;

        fetch(`/course/${id}/students_management/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error de red o servidor');
                }
                return response.text();
            })
            .then(html => {
                document.getElementById('modal-dialog-id').innerHTML = html;

                var draggedItem = null;

                document.addEventListener('dragstart', function(event) {
                    draggedItem = event.target;
                    event.dataTransfer.setData('text/plain', draggedItem.dataset.studentId);
                
                    if (draggedItem.classList.contains('no-students-message')) {
                        event.preventDefault();
                    }
                });
                
                document.addEventListener('dragover', function(event) {
                    event.preventDefault();
                });

                document.addEventListener('drop', function(event) {
                    if (event.target.classList.contains('list-group-item')) {
                        event.target.parentElement.insertBefore(draggedItem, event.target.nextSibling);
                    } else if (event.target.classList.contains('list-group')) {
                        event.target.appendChild(draggedItem);
                    }
                    draggedItem = null;
                
                    var enrolledStudents = document.querySelectorAll('#alumnosInscritos li');
                    var noStudentsMessage = document.querySelector('.no-students-message');
                
                    if (enrolledStudents.length > 0 && noStudentsMessage) {
                        noStudentsMessage.remove();
                    }
                
                    if (enrolledStudents.length === 0 && !noStudentsMessage) {
                        var ul = document.getElementById('alumnosInscritos');
                        var li = document.createElement('li');
                        li.classList.add('no-students-message', 'list-group-item');
                        li.innerText = 'No students yet';
                        ul.appendChild(li);
                    }
                });

                var items = document.querySelectorAll('#todosAlumnos li, #alumnosInscritos li');

                items.forEach(function(item) {
                    item.draggable = true;
                });

                var guardarCambiosButton = document.getElementById('guardarCambios');
                if (guardarCambiosButton) {
                    guardarCambiosButton.addEventListener('click', function() {
                        const courseId = this.value;

                        var enrolledStudents = document.querySelectorAll('#alumnosInscritos li');
                        
                        var studentsData = [];
                        
                        if (enrolledStudents.length === 1 && enrolledStudents[0].classList.contains('no-students-message')) {
                            enrolledStudents[0].remove();
                        } else {
                            enrolledStudents.forEach(function(student) {
                                studentsData.push({
                                    id: student.dataset.studentId
                                });
                            });
                        }

                        fetch(`/course/${courseId}/save_enrolled_students/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ students: studentsData })
                        })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Error de red o servidor');
                            }
                            return response.json();
                        })
                        .then(data => {
                            console.log('Cambios guardados con éxito:', data);

                            var modal = document.getElementById('myModal');
                            modal.style.display = 'none';
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                    });
                }

                document.querySelector('.close').addEventListener('click', function() {
                    modal.style.display = 'none';
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });

        modal.style.display = 'block';
    });
});

function editStudentData(button) {
    const studentRow = button.parentElement.parentElement;

    const nombre = studentRow.querySelector('.nombre').textContent;
    const documento = studentRow.querySelector('.documento').textContent;
    const estudianteId = button.dataset.estudianteId;

    document.querySelector('table').style.display = 'none';
    document.getElementById('nav-del-students').style.display = 'none';
    document.getElementById('students-title').style.display = 'none';
    document.getElementById('add-students-button').style.display = 'none';

    const form = document.getElementById('edit-form');
    form.style.display = 'block';

    form.querySelector('#edit-nombre').value = nombre;
    form.querySelector('#edit-documento').value = documento;
    form.querySelector('#estudiante_id').value = estudianteId;
}

function saveStudentChanges() {
    const newNombre = document.getElementById('edit-nombre').value;
    const newDocumento = document.getElementById('edit-documento').value;
    const estudianteId = document.getElementById('estudiante_id').value;

    fetch('/save_changes_student/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            estudianteId: estudianteId,
            nombre: newNombre,
            documento: newDocumento
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cambios guardados con éxito:', data);
        window.location.href = 'students';
    })
    .catch(error => console.error('Error:', error));
}

function editTeacherData(button) {
    const teacherRow = button.parentElement.parentElement;

    const nombre = teacherRow.querySelector('.nombre').textContent;
    const documento = teacherRow.querySelector('.documento').textContent;
    const profesion = teacherRow.querySelector('.profesion').textContent;
    const teacherId = button.dataset.teacherId;

    document.querySelector('table').style.display = 'none';
    document.getElementById('nav-del-teachers').style.display = 'none';
    document.getElementById('teachers-title').style.display = 'none';
    document.getElementById('add-teachers-button').style.display = 'none';

    const form = document.getElementById('edit-form');
    form.style.display = 'block';

    form.querySelector('#edit-nombre').value = nombre;
    form.querySelector('#edit-documento').value = documento;
    form.querySelector('#edit-profesion').value = profesion;
    form.querySelector('#teacher_id').value = teacherId;

}

function saveTeacherChanges() {
    const newNombre = document.getElementById('edit-nombre').value;
    const newDocumento = document.getElementById('edit-documento').value;
    const newProfesion = document.getElementById('edit-profesion').value;
    const teacherId = document.getElementById('teacher_id').value;

    fetch('/save_changes_teacher/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            teacherId: teacherId,
            nombre: newNombre,
            documento: newDocumento,
            profesion: newProfesion
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cambios guardados con éxito:', data);
        window.location.href = 'teachers';
    })
    .catch(error => console.error('Error:', error));
}

function editCourseData(button) {
    const courseRow = button.parentElement.parentElement;

    const nombre = courseRow.querySelector('.nombre').textContent;
    const categoria = button.dataset.categoria;
    const fecha_inicio = courseRow.querySelector('.fecha_inicio').textContent;
    const fecha_fin = courseRow.querySelector('.fecha_fin').textContent;
    const temario = button.parentElement.parentElement.querySelector('a').getAttribute('href');
    const teacher = button.dataset.teacher;
    const courseId = button.dataset.courseId;

    document.querySelector('table').style.display = 'none';
    document.getElementById('nav-del-course').style.display = 'none';
    document.getElementById('course-title').style.display = 'none';
    document.getElementById('app-title').style.display = 'none';

    const form = document.getElementById('edit-form');
    form.style.display = 'block';

    form.querySelector('#edit-nombre').value = nombre;
    form.querySelector('#edit-categoria').value = categoria;
    form.querySelector('#edit-fecha_inicio').value = fecha_inicio;
    form.querySelector('#edit-fecha_fin').value = fecha_fin;
    form.querySelector('#edit-temario').value = temario;
    form.querySelector('#edit-teacher').value = teacher;
    form.querySelector('#course_id').value = courseId;
}

function saveCourseChanges() {
    const newNombre = document.getElementById('edit-nombre').value;
    const newCategoria = document.getElementById('edit-categoria').value;
    const newFechaInicio = document.getElementById('edit-fecha_inicio').value;
    const newFechaFin = document.getElementById('edit-fecha_fin').value;
    const newTemario = document.getElementById('edit-temario').value;
    const newTeacher = document.getElementById('edit-teacher').value;
    const courseId = document.getElementById('course_id').value;

    fetch('/save_changes_course/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            courseId: courseId,
            nombre: newNombre,
            categoria: newCategoria,
            fecha_inicio: newFechaInicio,
            fecha_fin: newFechaFin,
            temario: newTemario,
            teacher: newTeacher
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cambios guardados con éxito:', data);
        window.location.href = '';
    })
    .catch(error => console.error('Error:', error));
}

