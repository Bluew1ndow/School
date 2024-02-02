from django.db import models


class Teacher(models.Model):
    id = models.AutoField
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    aadhar_card_image = models.ImageField(upload_to='Teacher/aadhar', default="")
    capacity = models.IntegerField()
    enrolled = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"

class Student(models.Model):
    id = models.AutoField
    rollNo = models.IntegerField(unique=True,default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class_name = models.IntegerField(default=0)
    date_of_admission = models.DateField()
    date_of_birth = models.DateField()
    birth_certificate = models.ImageField(upload_to='Student/birth_certificate', default="")
    address = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"

class Guardian(models.Model):
    id = models.AutoField
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Subject(models.Model):
    id = models.AutoField
    subject_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} (ID: {self.id})"


class Teacher_Subject_Assignment(models.Model):
    assignmentId = models.AutoField
    teacherId = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    subjectId = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Teacher: {self.teacherId}, Subject: {self.subjectId}"

