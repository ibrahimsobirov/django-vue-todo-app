from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages



@login_required
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


def login_view(request):
    if request.user.is_authenticated:
        return redirect('list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'tasks/login.html')



def register_view(request):
    if request.user.is_authenticated:
        return redirect('list')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = UserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


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


def api_task_update(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    data = json.loads(request.body)
    task = get_object_or_404(Task, id=task_id)
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.save()

    return JsonResponse({
        'status': 'success',
        'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'is_completed': task.is_completed,
        }
    })


def api_task_delete(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'status': 'success'})


def api_task_toggle(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()

    return JsonResponse({
        'status': 'success',
        'is_completed': task.is_completed,
    })

