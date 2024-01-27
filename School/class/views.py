from django.http import HttpResponse
from django.shortcuts import render
import json
from .models import Student , Guardian, Teacher, Subject,Teacher_Subject_Assignment
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger('file_log')


@csrf_exempt
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
            teacher = Teacher.objects.order_by('?')[0]
            student_obj.teacherId = teacher
            student_obj.save()

            guardian_obj = Guardian(
                name=data.get('guardian_name'),
                relation=data.get('guardian_relation'),
                phone_number=data.get('guardian_phone_number'),
                email_address=data.get('guardian_email_address'),
                studentId=student_obj
            )

            guardian_obj.save()


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
            guardians = Guardian.objects.filter(studentId=student)
            guardians.delete()

            student.delete()

            return JsonResponse({'message': 'Student and associated guardians deleted successfully!'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting student: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def getStudentDetails(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)

        guardians = Guardian.objects.filter(studentId=student)
        teacher = student.teacherId

        student_details = {
            'id': student.id,
            'rollNo': student.rollNo,
            'first_name': student.first_name,
            'middle_name': student.middle_name,
            'last_name': student.last_name,
            'class_name': student.class_name,
            'date_of_admission': student.date_of_admission,
            'date_of_birth': student.date_of_birth,
            'birth_certificate': student.birth_certificate,
            'address': student.address,
            'teacher': {
                'id': teacher.id,
                'first_name': teacher.first_name,
                'middle_name': teacher.middle_name,
                'last_name': teacher.last_name,
            },
            'guardians': [
                {
                    'id': guardian.id,
                    'name': guardian.name,
                    'relation': guardian.relation,
                    'phone_number': guardian.phone_number,
                    'email_address': guardian.email_address,
                }
                for guardian in guardians
            ],
        }

        return JsonResponse(data = {'student_details': student_details}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching student details: {str(e)}'}, status=500)


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
def addParentToStudent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            guardian_obj= Guardian(
                studentId = student,
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

@csrf_exempt
def getParentInformation(request, student_id):
    try:
        student = Student.objects.get(rollNo=student_id)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    if request.method == 'GET':
        try:
            guardians = Guardian.objects.filter(studentId=student)
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

            print(guardians_data)
            return JsonResponse({'parents': guardians_data})
        except Exception as e:
            return JsonResponse({'error': f'Error fetching parent information: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def getTeachersFiltered(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        subject_name = data.get('subject_name')
        subject = Subject.objects.get(subject_name=subject_name)
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)

    if request.method == 'GET':
        try:

            teachers = Teacher_Subject_Assignment.objects.filter(subjectId=subject).values('teacherId__id',
                                                                                           'teacherId__first_name')
            teachers_data = [
                {
                    'id': teacher['teacherId__id'],
                    'name': teacher['teacherId__first_name']
                }
                for teacher in teachers
            ]

            print(teachers_data)

            return JsonResponse({'teachers': teachers_data})
        except Exception as e:
            return JsonResponse({'error': f'Error fetching filtered teachers: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
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
                'aadhar_card_image': teacher.aadhar_card_image,
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
            students_assigned = Student.objects.filter(teacherId=teacher).values(
                'rollNo', 'first_name', 'middle_name', 'last_name', 'class_name',
                'date_of_admission', 'date_of_birth', 'birth_certificate', 'address'
            )

            for student in students_assigned:
                print(student)
            for student in list(students_assigned):
                print(student)

            return JsonResponse({'students_assigned': list(students_assigned)})
        except Exception as e:
            return JsonResponse({'error': f'Error fetching assigned students: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)