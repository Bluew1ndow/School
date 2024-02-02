from django.http import HttpResponse
from django.shortcuts import render
import json
from .models import Student , Guardian, Teacher, Subject,Teacher_Subject_Assignment
from django.http import JsonResponse
from django.db.models import Q
import logging
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger('file_log')

def index(request):
    return HttpResponse("Class")

@csrf_exempt
def addStudent(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            student_obj = Student(
                rollNo = data.get("roll_no"),
                first_name = data.get('student_first_name'),
                middle_name = data.get('student_middle_name'),
                last_name = data.get('student_last_name'),
                class_name = data.get('student_class_name'),
                date_of_admission = data.get('student_date_of_admission'),
                date_of_birth = data.get('student_date_of_birth'),
                birth_certificate = data.get('student_birth_certificate'),
                address = data.get('student_address'),
            )

            guardian_obj = Guardian(
                name=data.get('guardian_name'),
                relation=data.get('guardian_relation'),
                phone_number=data.get('guardian_phone_number'),
                email_address=data.get('guardian_email_address'),
                student=student_obj
            )
            # teacher = Teacher.objects.order_by('?')[0]

            teachers = Teacher.objects.all()
            for teacher in teachers:
                print (teacher)
                if (teacher.enrolled < teacher.capacity):
                    teacher.enrolled += 1
                    student_obj.teacher = teacher
                    try:
                        # To Check Previous Students assigned to Teacher
                        # for student in students:
                        #     if student.teacherId.id == teacher.id:
                        #         print(student)

                        student_obj.save()
                        guardian_obj.save()
                        teacher.save()
                        break
                    except Exception as e:
                        return  JsonResponse({'message':'Cannot assign Teacher'})

            return JsonResponse({'message': 'Student added successfully!'})
        except Exception as e:
            return JsonResponse({'error': f'Error adding student: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def editStudent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))

            student.rollNo = data.get('rollNo',student.rollNo)
            student.first_name = data.get('first_name', student.first_name)
            student.middle_name = data.get('middle_name', student.middle_name)
            student.last_name = data.get('last_name', student.last_name)
            student.class_name = data.get('class_name', student.class_name)
            student.date_of_admission = data.get('date_of_admission', student.date_of_admission)
            student.date_of_birth = data.get('date_of_birth', student.date_of_birth)
            student.birth_certificate = data.get('birth_certificate', student.birth_certificate)
            student.address = data.get('address', student.address)

            teacher_id = data.get('teacher')
            prev_teacher = student.teacher
            if (teacher_id is not None) and (teacher_id != prev_teacher.id):
                try:
                    teacher = Teacher.objects.get(pk=teacher_id)
                    teacher.enrolled += 1
                    student.teacher.enrolled -= 1
                    prev_teacher.save()
                    teacher.save()
                    student.teacher = teacher
                except Teacher.DoesNotExist:
                    return JsonResponse({'error': 'Invalid teacher ID'}, status=400)

            student.save()

            return JsonResponse(data = {'message': 'Student information updated successfully!'},status=200)

        except Exception as e:
            return JsonResponse(data = {'error': f'Error updating student information: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
@csrf_exempt
def deleteStudent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    if request.method == 'DELETE':
        try:
            teacher = student.teacher
            teacher.enrolled -= 1
            guardians = Guardian.objects.flter(student=student)

            teacher.save()

            guardians.delete()
            student.delete()

            return JsonResponse({'message': 'Student and associated guardians deleted successfully!'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting student: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def getAllStudents(request, class_name):
    try:
        students = Student.objects.filter(class_name = class_name).select_related('teacher').prefetch_related('guardian_set')

        student_details = [
            {
                'id': student.id,
                'rollNo': student.rollNo,
                'first_name': student.first_name,
                'middle_name': student.middle_name,
                'last_name': student.last_name,
                'class_name': student.class_name,
                'date_of_admission': student.date_of_admission,
                'date_of_birth': student.date_of_birth,
                # Commented for now as default is nothing
                'birth_certificate': student.birth_certificate.url if student.birth_certificate else None,
                'address': student.address,
                'teacher': {
                    'id': student.teacher.id,
                    'first_name': student.teacher.first_name,
                    'middle_name': student.teacher.middle_name,
                    'last_name': student.teacher.last_name,
                    'aadhar_card_image': student.teacher.aadhar_card_image.url if student.teacher.aadhar_card_image else None,
                    'enrolled': student.teacher.enrolled,
                    'capacity': student.teacher.capacity
                },
                'guardians': [
                    {
                        'id': guardian.id,
                        'name': guardian.name,
                        'relation': guardian.relation,
                        'phone_number': guardian.phone_number,
                        'email_address': guardian.email_address,
                    }
                    for guardian in student.guardian_set.all()
                ],
            }
            for student in students
        ]

        return JsonResponse(data = {'student_details': student_details}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching student details: {str(e)}'}, status=500)

def getStudentDetails(request, student_id):
    try:
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        student_details = {
            'id': student.id,
            'rollNo': student.rollNo,
            'first_name': student.first_name,
            'middle_name': student.middle_name,
            'last_name': student.last_name,
            'class_name': student.class_name,
            'date_of_admission': student.date_of_admission,
            'date_of_birth': student.date_of_birth,
            'birth_certificate': student.birth_certificate.url if student.birth_certificate else None,
            'address': student.address,
            'teacher': {
                'id': student.teacher.id,
                'first_name': student.teacher.first_name,
                'middle_name': student.teacher.middle_name,
                'last_name': student.teacher.last_name,
                'aadhar_card_image': student.teacher.aadhar_card_image.url if student.teacher.aadhar_card_image else None,
                'enrolled': student.teacher.enrolled,
                'capacity': student.teacher.capacity
            },
            'guardians': [
                {
                    'id': guardian.id,
                    'name': guardian.name,
                    'relation': guardian.relation,
                    'phone_number': guardian.phone_number,
                    'email_address': guardian.email_address,
                }
                for guardian in student.guardian_set.all()
            ],
        }

        return JsonResponse(data={'student_details': student_details}, status=200)

    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': f'Error fetching student details: {str(e)}'}, status=500)






@csrf_exempt
def addParentToStudent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            guardian_obj= Guardian(
                student = student,
                name = data.get('name'),
                relation = data.get('relation'),
                phone_number = data.get('phone_number'),
                email_address = data.get('email_address'),
            )

            guardian_obj.save()

            return JsonResponse({'message': 'Parent added to student successfully!'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error adding parent to student: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def editParent(request, parent_id):
    try:
        guardian = Guardian.objects.get(pk=parent_id)
    except Guardian.DoesNotExist:
        return JsonResponse({'error': 'Parent not found'}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            guardian.name = data.get('name', guardian.name)
            guardian.relation = data.get('relation', guardian.relation)
            guardian.phone_number = data.get('phone_number', guardian.phone_number)
            guardian.email_address = data.get('email_address', guardian.email_address)
            guardian.save()

            return JsonResponse({'message': 'Parent information updated successfully!'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error updating parent information: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def deleteParent(request, parent_id):
    try:
        guardian = Guardian.objects.get(pk=parent_id)
    except Guardian.DoesNotExist:
        return JsonResponse({'error': 'Parent not found'}, status=404)

    if request.method == 'DELETE':
        try:
            guardian.delete()
            return JsonResponse({'message': 'Parent information deleted successfully!'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting parent information: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def getParentInformation(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    if request.method == 'GET':
        try:
            guardians = Guardian.objects.filter(student=student)
            guardians_data = [
                {
                    'id': guardian.id,
                    'name': guardian.name,
                    'relation': guardian.relation,
                    'phone_number': guardian.phone_number,
                    'email_address': guardian.email_address,
                }
                for guardian in guardians
            ]

             # print(guardians_data)
            return JsonResponse({'parents': guardians_data})
        except Exception as e:
            return JsonResponse({'error': f'Error fetching parent information: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def addTeacher(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            teacher = Teacher.objects.create(
                first_name = data.get('first_name'),
                middle_name = data.get('middle_name'),
                last_name = data.get('last_name'),
                date_of_birth = data.get('date_of_birth'),
                # Check this
                aadhar_card_image = data.get('aadhar_card_image'),
                capacity = data.get('capacity'),
            )

            subjects_data = data.get('subjects',[])
            for subject_data in subjects_data:
                subject,created = Subject.objects.get_or_create(
                    subject_name = subject_data.get('subject_name')
                )

                Teacher_Subject_Assignment.objects.create(
                    teacherId = teacher,
                    subjectId = subject
                )


            return JsonResponse(data = {'message': 'Teacher added successfully!'} , status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error adding teacher: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def editTeacher(request, teacher_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            teacher = Teacher.objects.get(pk=teacher_id)

            current_capacity = teacher.capacity
            new_capacity = data.get('capacity')

            teacher.first_name = data.get('first_name', teacher.first_name)
            teacher.middle_name = data.get('middle_name', teacher.middle_name)
            teacher.last_name = data.get('last_name', teacher.last_name)
            teacher.date_of_birth = data.get('date_of_birth', teacher.date_of_birth)
            teacher.aadhar_card_image = data.get('aadhar_card_image', teacher.aadhar_card_image)
            teacher.capacity = new_capacity

            # If the new capacity is lower, reassign students to other teachers
            if (teacher.enrolled > new_capacity):
                students_to_reassign = teacher.student_set.all()[:(teacher.enrolled - new_capacity)]
                other_teachers = Teacher.objects.exclude(pk = teacher_id)


                # Assigning Linearly without Sorting, could be modified later
                i = 0
                for student in students_to_reassign:
                    while (i < len(other_teachers)) and (other_teachers[i].enrolled == other_teachers[i].capacity):
                        i += 1

                    if i < len(other_teachers):
                        # print(student)
                        new_teacher = other_teachers[i]

                        student.teacher.enrolled -= 1
                        student.teacher.save()

                        new_teacher.enrolled += 1
                        new_teacher.save()

                        student.teacher = new_teacher
                        student.save()
                    else:
                        print("Not enough teachers with available capacity.")

            teacher.save()

            return JsonResponse({'message': 'Teacher information updated successfully!'}, status=200)

        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Teacher not found'}, status=404)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error updating teacher information: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def deleteTeacher(request, teacher_id):
    if request.method == 'DELETE':
        try:
            teacher_to_delete = Teacher.objects.get(pk = teacher_id)
            other_teachers = Teacher.objects.exclude(pk = teacher_id)
            students_to_reassign = teacher_to_delete.student_set.all()
            print(students_to_reassign)

            i = 0
            for student in students_to_reassign:
                while (i < len(other_teachers)) and (other_teachers[i].enrolled == other_teachers[i].capacity):
                    i += 1

                if i < len(other_teachers):
                    # print(student)
                    new_teacher = other_teachers[i]
                    new_teacher.enrolled += 1
                    new_teacher.save()

                    student.teacher = new_teacher
                    student.save()
                else:
                    print("Not enough teachers with available capacity.")

            teacher_to_delete.delete()

            return JsonResponse({'message': f'Teacher deleted. {students_to_reassign} students reassigned.'},
                            status=200)

        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Teacher not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error deleting teacher: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.http import JsonResponse
from django.db.models import Q

def getTeachersFiltered(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        capacity = data.get('capacity', None)
        subject_id = data.get('subject_id',None)
        teachers = []
        # print(capacity)
        teachers_query = Q()

        if subject_id:
            teachers_query &= Q(teacher_subject_assignment__subjectId=subject_id)

        if capacity:
            teachers_query &= Q(capacity=capacity)

        teachers = Teacher.objects.filter(teachers_query).distinct()

        teachers_data = [
            {
                'id': teacher.id,
                'first_name': teacher.first_name,
                'middle_name': teacher.middle_name,
                'last_name': teacher.last_name,
                'capacity': teacher.capacity,
                'enrolled': teacher.enrolled
            }
            for teacher in teachers
        ]

        return JsonResponse({'teachers': teachers_data})
    except Exception as e:
        return JsonResponse({'error': f'Error fetching filtered teachers: {str(e)}'}, status=500)



def getTeacherDetails(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher not found'}, status=404)

    if request.method == 'GET':
        try:
            teacher_details = {
                'id': teacher.id,
                'first_name': teacher.first_name,
                'middle_name': teacher.middle_name,
                'last_name': teacher.last_name,
                'date_of_birth': teacher.date_of_birth,
                'aadhar_card_image': teacher.aadhar_card_image.url,
                'capacity': teacher.capacity,
                'created_at': teacher.created_at,
                'modified_at': teacher.modified_at,
            }

            return JsonResponse({'teacher_details': teacher_details})
        except Exception as e:
            return JsonResponse({'error': f'Error fetching teacher details: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def getStudentsAssignedToTeacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher not found'}, status=404)

    if request.method == 'GET':
        try:
            students_assigned = Student.objects.filter(teacher=teacher).values(
                'rollNo', 'first_name', 'middle_name', 'last_name', 'class_name',
                'date_of_admission', 'date_of_birth', 'birth_certificate', 'address'
            )

            # for student in students_assigned:
            #     print(student)
            # for student in list(students_assigned):
            #     print(student)

            return JsonResponse({'students_assigned': list(students_assigned)})
        except Exception as e:
            return JsonResponse({'error': f'Error fetching assigned students: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)