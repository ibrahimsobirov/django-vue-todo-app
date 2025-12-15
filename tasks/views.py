from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.http import JsonResponse
import json


def list(request):
    return render(request, 'tasks/list.html')


def api_get_list(request):
    tasks = Task.objects.all()
    response_data = []
    for task in tasks:
        response_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'is_completed': task.is_completed,
        })
    return JsonResponse(response_data, safe=False)


def api_task_create(request):
    data = json.loads(request.body)
    
    title = data['title']
    description = data.get('description', '')

    task = Task.objects.create(title=title, description=description)
    return JsonResponse({
        'status': 'success', 
        'task': {
            'id': task.id, 
            'title': task.title, 
            'description': task.description, 
            'is_completed': task.is_completed
        }
    })

