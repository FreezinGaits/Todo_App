from django.shortcuts import render
from todo.models import Task

def home(request):
  task =  Task.objects.filter(is_completed=False).order_by('-updated_at')
  completed_task = Task.objects.filter(is_completed=True).order_by('-updated_at')
  context = {'tasks': task, 'completed_tasks': completed_task}
  return render(request, 'home.html', context)