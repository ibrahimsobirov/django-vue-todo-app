from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskImage
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import base64
import uuid
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import os



def debug_log(location, message, data, hypothesis_id='H4'):
    """Helper function to write debug logs"""
    try:
        import json as json_module
        log_data = {
            'location': location,
            'message': message,
            'data': data,
            'timestamp': int(__import__('time').time() * 1000),
            'sessionId': 'debug-session',
            'runId': 'run1',
            'hypothesisId': hypothesis_id
        }
        log_path = '/home/ibrahim/django-vue-todo-app/.cursor/debug.log'
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a') as f:
            f.write(json_module.dumps(log_data) + '\n')
    except Exception:
        pass 

@login_required
def list(request):
    return render(request, 'tasks/list.html')


@login_required
def api_get_list(request):
    tasks = Task.objects.filter(user=request.user)

    return JsonResponse([
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'is_completed': t.is_completed,
            'thumbnail': t.image.url if t.image else None,
            'image': t.image.url if t.image else None,
            'images': ([ti.image.url for ti in t.images.all()] or ([t.image.url] if t.image else []))
        }
        for t in tasks
    ], safe=False)


def login_view(request):
    return render(request, 'tasks/login.html')


@csrf_exempt
def login_api(request):
    
    debug_log('views.py:login_api()', 'Login API called',
              {'method': request.method}, 'H4')
    try:
        if not request.body:
            debug_log('views.py:login_api()', 'Empty request body', {}, 'H4')
            return JsonResponse({'status': 'error', 'message': 'Request body is required.'}, status=400)
        data = json.loads(request.body)
        debug_log('views.py:login_api()', 'Request body parsed', {'username': data.get(
            'username', ''), 'hasPassword': bool(data.get('password'))}, 'H4')
        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            debug_log('views.py:login_api()', 'Missing username or password', {
                      'hasUsername': bool(username), 'hasPassword': bool(password)}, 'H4')
            return JsonResponse({'status': 'error', 'message': 'Username and password are required.'}, status=400)

        user = authenticate(request, username=username, password=password)
        debug_log('views.py:login_api()', 'Authentication result', {
                  'userAuthenticated': user is not None, 'userId': user.id if user else None}, 'H4')

        if user is not None:
            login(request, user)
            debug_log('views.py:login_api()', 'User logged in', {
                      'userId': user.id, 'username': user.username}, 'H5')
            return JsonResponse({'status': 'success'})
        else:
            debug_log('views.py:login_api()', 'Authentication failed', {
                      'username': username}, 'H4')
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'})
    except Exception as e:
        debug_log('views.py:login_api()', 'Login API exception', {
                  'error': str(e), 'errorType': type(e).__name__}, 'H4')
        return JsonResponse({'status': 'error', 'message': 'An error occurred during login.'})


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


@csrf_exempt
def register_api(request):
    debug_log('views.py:register_api()', 'Register API called',
              {'method': request.method}, 'H4')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            debug_log('views.py:register_api()', 'Request body parsed', {'username': data.get(
                'username', ''), 'hasPassword1': bool(data.get('password1')), 'hasPassword2': bool(data.get('password2'))}, 'H4')
            username = data.get('username', '').strip()
            password1 = data.get('password1', '').strip()
            password2 = data.get('password2', '').strip()

            if not username:
                debug_log('views.py:register_api()',
                          'Validation failed: username empty', {}, 'H4')
                return JsonResponse({'status': 'error', 'message': 'Username is required.'})
            if not password1:
                debug_log('views.py:register_api()',
                          'Validation failed: password empty', {}, 'H4')
                return JsonResponse({'status': 'error', 'message': 'Password is required.'})
            if password1 != password2:
                debug_log('views.py:register_api()',
                          'Validation failed: passwords do not match', {}, 'H4')
                return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})

            if User.objects.filter(username=username).exists():
                debug_log('views.py:register_api()', 'Validation failed: username exists', {
                          'username': username}, 'H4')
                return JsonResponse({'status': 'error', 'message': 'Username already exists.'})

            user = User.objects.create_user(
                username=username, password=password1)
            debug_log('views.py:register_api()', 'User created', {
                      'userId': user.id, 'username': user.username}, 'H4')
            login(request, user)
            debug_log('views.py:register_api()', 'User logged in after registration', {
                      'userId': user.id}, 'H5')
            return JsonResponse({'status': 'success', 'message': 'Registration successful!'})

        except json.JSONDecodeError as e:
            debug_log('views.py:register_api()',
                      'JSON decode error', {'error': str(e)}, 'H4')
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
        except Exception as e:
            debug_log('views.py:register_api()', 'Register API exception', {
                      'error': str(e), 'errorType': type(e).__name__}, 'H4')
            return JsonResponse({'status': 'error', 'message': 'Registration failed.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def api_task_create(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            images_data = request.POST.getlist('images')
            image_data = request.POST.get('image')

            task = Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                is_completed=False
            )

            if not images_data and image_data:
                images_data = [image_data]

            first_task_image = None
            for index, one_image_data in enumerate(images_data):
                if not (isinstance(one_image_data, str) and one_image_data.startswith('data:image')):
                    continue

                format, imgstr = one_image_data.split(';base64,')
                ext = format.split('/')[-1]
                filename = f'task_{uuid.uuid4()}.{ext}'
                data = ContentFile(base64.b64decode(imgstr), name=filename)

                task_image = TaskImage(task=task, order=index)
                task_image.image.save(filename, data, save=True)

                if first_task_image is None:
                    first_task_image = task_image

            if first_task_image is not None:
                task.image = first_task_image.image
                task.save(update_fields=['image'])

            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'is_completed': task.is_completed,
                'thumbnail': task.image.url if task.image else None,
                'image': task.image.url if task.image else None,
                'images': ([ti.image.url for ti in task.images.all()] or ([task.image.url] if task.image else []))
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def api_task_update(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    task = get_object_or_404(Task, id=task_id)

    if request.content_type == 'application/json':
        data = json.loads(request.body)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.save()
    else:
        task.title = request.POST.get('title', task.title).strip()
        task.description = request.POST.get(
            'description', task.description).strip()

        images_data = request.POST.getlist('images')

        image_data = request.POST.get('image')

        if images_data:
            task.images.all().delete()
            first_task_image = None
            for index, one_image_data in enumerate(images_data):
                if not (isinstance(one_image_data, str) and one_image_data.startswith('data:image')):
                    continue

                format, imgstr = one_image_data.split(';base64,')
                ext = format.split('/')[-1]
                filename = f'task_{uuid.uuid4()}.{ext}'
                data = ContentFile(base64.b64decode(imgstr), name=filename)

                task_image = TaskImage(task=task, order=index)
                task_image.image.save(filename, data, save=True)

                if first_task_image is None:
                    first_task_image = task_image

            if first_task_image is not None:
                task.image = first_task_image.image
            else:
                if task.image:
                    task.image.delete(save=False)
                task.image = None

        elif image_data:
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]

                filename = f'task_{uuid.uuid4()}.{ext}'

                data = ContentFile(base64.b64decode(imgstr), name=filename)
                task.image.save(filename, data, save=True)
            elif image_data == '':  
                if task.image:
                    task.image.delete()
        elif request.POST.get('remove_image') == 'true':
            if task.image:
                task.image.delete()
            task.images.all().delete()

        task.save()

    return JsonResponse({
        'status': 'success',
        'task': {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'is_completed': task.is_completed,
            'thumbnail': task.image.url if task.image else None,
            'image': task.image.url if task.image else None,
            'images': ([ti.image.url for ti in task.images.all()] or ([task.image.url] if task.image else []))
        }
    })


@login_required
def api_task_delete(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'status': 'success'})


@login_required
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


def decode_base64_image(data):
    if not data:
        return None

    if ';base64,' not in data:
        raise ValueError('Invalid base64 image')

    header, encoded = data.split(';base64,')
    file_ext = header.split('/')[-1]

    if file_ext not in ['png', 'jpg', 'jpeg']:
        raise ValueError('Unsupported image type')

    file_name = f"{uuid.uuid4()}.{file_ext}"
    decoded_file = base64.b64decode(encoded)

    return ContentFile(decoded_file, name=file_name)
