from django.http import HttpResponse
from django.shortcuts import render

def index(reqeust):
    return HttpResponse("Class")
def addStudent(reqeust):
    data = request.data