from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/tasks.html', {'tasks': tasks})


def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        Task.objects.create(
            title=title,
            description=description,
        )
        return redirect('tasks')

    return render(request, 'tasks/create_task.html')


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})


def home(request):
    return HttpResponse("Welcome to the Task Management System")


def about(request):
    return HttpResponse("This is a simple task management application built with Django.")
