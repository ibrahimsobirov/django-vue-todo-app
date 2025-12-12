from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/list.html', {'tasks': tasks})


def task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')

        if title:
            Task.objects.create(title=title, description=description)
            return redirect('list')
        
    return render(request, 'tasks/create.html')


def detail(request, task_id):
    task_object = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/details.html', {'task': task_object})


def edit(request, task_id):
    task_object = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task_object.title = request.POST.get('title')
        task_object.description = request.POST.get('description', '')
        task_object.is_completed = (request.POST.get('is_completed') == 'on') 
        task_object.save()
        return redirect('details', task_id=task_id)
    return render(request, 'tasks/edit.html', {'task': task_object})


def delete(request, task_id):
    task_object = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task_object.delete()
        return redirect('list')

    return redirect('details', task_id=task_id)