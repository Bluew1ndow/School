from django.contrib import admin
from .models import Student, Teacher, Guardian, Subject

# Register your models here.
admin.site.register(Student);
admin.site.register(Teacher);
admin.site.register(Guardian);
admin.site.register(Subject);

