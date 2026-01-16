# AGENTS.md - Coding Guidelines for AI Agents

This document provides comprehensive guidelines for AI coding agents working on this Django + Vue.js todo application. It includes build/lint/test commands, code style conventions, and development practices.

## Project Overview

This is a Django backend with Vue.js frontend todo application featuring:
- User authentication and task management
- Image upload functionality
- RESTful API endpoints
- Bootstrap 5 UI with Vue.js 3

## Build, Lint, and Test Commands

### Python/Django Commands

```bash
# Activate virtual environment
source myvenv/bin/activate

# Install Python dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Run Django development server
python manage.py runserver

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run Django tests
python manage.py test

# Run specific test file
python manage.py test tasks.tests

# Run specific test method
python manage.py test tasks.tests.TestClass.test_method

# Check for Django system check warnings
python manage.py check

# Collect static files
python manage.py collectstatic --noinput
```

### JavaScript/Node.js Commands

**Note:** This project has a `package-lock.json` but no `package.json`. If npm scripts are needed:

```bash
# Install Node.js dependencies (if package.json exists)
npm install

# Run linting (if configured)
npm run lint

# Run tests (if configured)
npm run test

# Build for production (if configured)
npm run build
```

### Database Commands

```bash
# Reset database (WARNING: destroys all data)
rm db.sqlite3
python manage.py migrate

# Create database backup
cp db.sqlite3 db_backup.sqlite3
```

## Code Style Guidelines

### Python/Django Conventions

#### Imports
- Standard library imports first, then third-party, then local imports
- One import per line
- Group imports with blank lines between groups

```python
import os
import json
from pathlib import Path

from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Task
```

#### Naming Conventions
- **Classes**: PascalCase (`TaskModel`, `UserSerializer`)
- **Functions/Methods**: snake_case (`get_task_list`, `create_task`)
- **Variables**: snake_case (`task_list`, `user_id`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_LENGTH = 200`)
- **URLs**: kebab-case in URL patterns (`task-list`, `user-profile`)

#### Django Models
- Use descriptive field names
- Add help_text and verbose_name where helpful
- Include Meta class with ordering
- Implement `__str__` method

```python
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="Task title")
    description = models.TextField(blank=True, verbose_name="Task Description")
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
```

#### Views
- Use class-based views when possible (ModelViewSet, APIView)
- Keep view logic simple, delegate to services/forms
- Use appropriate HTTP status codes
- Handle exceptions properly

```python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class TaskListCreateView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### Error Handling
- Use try/except blocks for external operations
- Return appropriate JSON error responses
- Log errors for debugging

```python
try:
    task = Task.objects.get(id=task_id, user=request.user)
except Task.DoesNotExist:
    return Response(
        {"error": "Task not found"},
        status=status.HTTP_404_NOT_FOUND
    )
```

### JavaScript/Vue.js Conventions

#### Vue.js Components
- Use Composition API with `<script setup>` syntax
- Use kebab-case for component file names
- Use PascalCase for component names in templates

```javascript
// task-item.vue
<script setup>
import { ref } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['toggle', 'delete'])

const toggleTask = () => {
  emit('toggle', props.task.id)
}
</script>

<template>
  <div class="task-item">
    <h3>{{ task.title }}</h3>
    <button @click="toggleTask">
      {{ task.completed ? 'Mark Incomplete' : 'Mark Complete' }}
    </button>
  </div>
</template>
```

#### JavaScript Best Practices
- Use `const` and `let` instead of `var`
- Use arrow functions for callbacks
- Handle promises with async/await
- Use descriptive variable names

```javascript
const handleTaskCreation = async () => {
  try {
    const response = await fetch('/api/tasks/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(taskData)
    })

    if (!response.ok) {
      throw new Error('Failed to create task')
    }

    const newTask = await response.json()
    tasks.value.push(newTask)
  } catch (error) {
    console.error('Error creating task:', error)
    alert('Failed to create task. Please try again.')
  }
}
```

### HTML/Django Templates

#### Template Structure
- Use semantic HTML5 elements
- Follow Django template naming conventions
- Use template inheritance
- Include CSRF tokens in forms

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>
    {% block content %}{% endblock %}
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>

<!-- task_list.html -->
{% extends 'base.html' %}

{% block title %}Task List{% endblock %}

{% block content %}
<div class="container">
    <h1>My Tasks</h1>
    {% for task in tasks %}
        <div class="task-item">
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
        </div>
    {% endfor %}
</div>
{% endblock %}
```

### Database and API Design

#### API Endpoints
- Use RESTful naming conventions
- Include version in URL paths (`/api/v1/tasks/`)
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Return consistent JSON response formats

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/tasks/', views.TaskListView.as_view(), name='task-list'),
    path('api/tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/<int:pk>/toggle/', views.TaskToggleView.as_view(), name='task-toggle'),
]
```

#### Security Best Practices

#### Django Security
- Always use `{% csrf_token %}` in forms
- Validate user input on both frontend and backend
- Use Django's built-in authentication
- Sanitize file uploads
- Use environment variables for secrets

```python
# settings.py
import os

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# For production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

#### File Upload Security
- Validate file types and sizes
- Use secure file naming
- Store uploads outside web root
- Scan for malware if applicable

```python
def validate_image(file):
    if file.size > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("Image too large")
    if not file.content_type in ['image/jpeg', 'image/png']:
        raise ValidationError("Invalid image type")
```

### Testing Guidelines

#### Django Tests
- Use descriptive test method names
- Test both success and failure cases
- Use factories for test data creation
- Test API endpoints with Django REST framework's test client

```python
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_create_task(self):
        """Test creating a new task"""
        data = {
            'title': 'Test Task',
            'description': 'Test Description'
        }
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_create_task_without_title(self):
        """Test creating a task without required title"""
        data = {'description': 'Test Description'}
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

### Development Workflow

#### Git Workflow
- Use feature branches for new development
- Write clear commit messages
- Squash commits before merging
- Use pull requests for code review

```bash
# Feature development workflow
git checkout -b feature/add-task-search
# Make changes
git add .
git commit -m "Add search functionality to task list"
git push origin feature/add-task-search
# Create pull request
```

#### Code Review Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] No console.log statements in production code
- [ ] Sensitive data not logged
- [ ] Database migrations included
- [ ] Documentation updated

### Performance Considerations

#### Frontend Optimization
- Minimize Vue.js re-renders with proper key usage
- Use lazy loading for images
- Debounce search inputs
- Cache API responses when appropriate

#### Backend Optimization
- Use select_related and prefetch_related for database queries
- Implement pagination for large datasets
- Use Django's caching framework
- Optimize database indexes

### Deployment

#### Environment Setup
- Use environment variables for configuration
- Separate settings for development/production
- Use proper SECRET_KEY in production
- Configure static file serving

#### Production Checklist
- [ ] DEBUG = False
- [ ] SECRET_KEY from environment
- [ ] Database credentials secured
- [ ] Static files collected
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Logging configured

## Tool Integration

### No Linting Tools Configured
Currently, no ESLint, Prettier, Black, or Flake8 configuration exists. When adding linting:

1. Install tools: `pip install black flake8 isort`
2. Create configuration files
3. Add npm scripts for frontend linting
4. Run linters before commits

### IDE Configuration
- Use Python extension for VS Code/PyCharm
- Configure Vue.js extension for frontend development
- Set up Django extensions for better development experience

## Common Patterns

### Error Response Format
```json
{
  "error": "Descriptive error message",
  "code": "ERROR_CODE"
}
```

### Success Response Format
```json
{
  "status": "success",
  "data": { ... },
  "message": "Optional success message"
}
```

### Pagination Response
```json
{
  "count": 100,
  "next": "http://api.example.com/tasks/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

This document should be updated as the project evolves and new tools or conventions are adopted.</content>
<parameter name="filePath">/home/ibrahim/django-vue-todo-app/AGENTS.md