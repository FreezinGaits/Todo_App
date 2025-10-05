from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task

# Create your views here.
def addTask(request):
  # print(request.POST) # <QueryDict: {'csrfmiddlewaretoken': ['ohqmCT47B3kSLr7E9UdWmZLJ7m4wGl7LCMjiCzJsHXMUWVrWqzhN7naZh2bOn9sT'], 'task': ['Hey boi!']}>, task is input field name attribute
  # print(request.POST['task']) # Hey boi!
  task = request.POST['task']
  Task.objects.create(task = task)
  return redirect('home')
  # return HttpResponse('The form is submitted')