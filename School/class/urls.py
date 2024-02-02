from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_student/', views.addStudent),
    path('edit_student/<int:student_id>/', views.editStudent, name='edit_student'),
    path('delete_student/<int:student_id>/', views.deleteStudent, name='delete_student'),
    path('get_all_students/<int:class_name>/', views.getAllStudents, name='get_all_students'),
    path('get_student_details/<int:student_id>/', views.getStudentDetails, name='get_student_details'),
    path('add_parent_to_student/<int:student_id>/', views.addParentToStudent, name='add_parent_to_student'),
    path('edit_parent/<int:parent_id>/', views.editParent, name='edit_parent'),
    path('delete_parent/<int:parent_id>/', views.deleteParent, name='delete_parent'),
    path('get_parent_information/<int:student_id>/', views.getParentInformation, name='get_parent_information'),
    path('add_teacher/', views.addTeacher, name='add_teacher'),
    path('edit_teacher/<int:teacher_id>/', views.editTeacher, name='edit_teacher'),
    path('delete_teacher/<int:teacher_id>/', views.deleteTeacher, name='delete_teacher'),
    path('get_teachers_filtered/', views.getTeachersFiltered, name='get_teachers_filtered'),
    path('get_teacher_details/<int:teacher_id>/', views.getTeacherDetails, name='get_teacher_details'),
    path('get_students_assigned/<int:teacher_id>/', views.getStudentsAssignedToTeacher, name='get_students_assigned'),

]