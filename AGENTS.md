# AGENTS.md

This document provides essential information for AI agents working on this Django + Vue.js Todo application.

## Project Overview

**Django 6.0.1 + Vue.js 3 + Bootstrap 5** todo application with image upload support.

- **Backend**: Django with built-in authentication, SQLite database
- **Frontend**: Vue.js 3 (CDN-loaded in templates), no build step
- **API**: RESTful JSON endpoints for task operations
- **Images**: Base64 encoding for JSON transmission, stored in `media/tasks/`

**Key Components:**
- `tasks/` - Django app (models, views, URLs)
- `templates/tasks/` - HTML templates with Vue.js components
- `media/tasks/` - Uploaded task images
- `db.sqlite3` - SQLite database

## Build/Test/Lint Commands

### Development Server
```bash
source myvenv/bin/activate
python manage.py runserver
```

### Running Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test tasks

# Specific test class
python manage.py test tasks.tests.TestClassName

# Specific test method
python manage.py test tasks.tests.TestClassName.test_method_name

# Verbose output
python manage.py test --verbosity 2
```

### Database Migrations
```bash
python manage.py makemigrations    # Create migrations
python manage.py migrate           # Apply migrations
python manage.py showmigrations    # Show status
```

### Code Quality
```bash
# Install tools (not currently in project)
pip install black flake8 mypy isort

# Format code
black .

# Lint
flake8 tasks/ todo/

# Type check (Django requires specific mypy config)
mypy tasks/ todo/

# Sort imports
isort tasks/ todo/
```

## Code Style Guidelines

### Python/Django

#### Imports
- Standard library → Third-party → Local (alphabetically)
```python
import json
import os
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Task, TaskImage
```

#### Formatting
- **Line length**: 100 characters
- **Indentation**: 4 spaces
- **Quotes**: Single quotes for strings
- **Trailing commas**: Use in multi-line structures

#### Naming
- **Classes**: PascalCase (`Task`, `TaskImage`)
- **Functions/Methods**: snake_case (`api_task_create`)
- **Variables**: snake_case (`task_id`, `is_completed`)
- **Constants**: UPPER_SNAKE_CASE
- **Private**: Prefix with `_`

#### Type Hints
```python
from typing import List, Optional, Dict, Any

def get_tasks(user_id: int) -> List['Task']:
    pass

def create_task(
    title: str,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    pass
```

#### Error Handling
- Use specific exception types
- Use `get_object_or_404` for views
- Return meaningful JSON error responses
- Log errors to `.cursor/debug.log`

```python
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

def api_task_update(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
        data = json.loads(request.body)
        # ... update logic
        return JsonResponse({'status': 'success'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

#### Django-Specific Patterns
- **Views**: Use `@login_required` for protected views
- **API Views**: Use `@csrf_exempt` for JSON endpoints from Vue.js
- **Models**: Define `__str__` methods, proper `Meta` classes
- **URLs**: Use `name` parameter for reverse URL lookup
- **QuerySets**: Use `filter()` over `all()` when possible

```python
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
```

#### Security
- Never commit secrets (API keys, passwords)
- Validate all user input
- Sanitize file uploads (type/size checks)
- Use CSRF tokens for forms
- Set `DEBUG=False` in production

### Vue.js/Frontend

#### JavaScript Style
- Use `const`/`let` over `var`
- Arrow functions for callbacks
- Template literals for strings
- Async/await for promises

```javascript
const fetchData = async () => {
  try {
    const response = await fetch('/api/tasks/');
    const data = await response.json();
    this.tasks = data;
  } catch (error) {
    console.error('Error:', error);
  }
};
```

#### Vue.js Patterns
- Use `v-for` with `:key`
- Use `v-model` for two-way binding
- Handle errors in fetch calls
- Use loading states

```javascript
methods: {
  async toggleTask(task) {
    try {
      const response = await fetch(`/api/tasks/${task.id}/toggle/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': this.csrfToken }
      });
      const data = await response.json();
      task.is_completed = data.is_completed;
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to update task');
    }
  }
}
```

#### Image Handling
- Convert to base64 for JSON transmission
- Use `FileReader` API client-side
- Validate file types and sizes (client + server)
- Display thumbnails for better UX

### Git/Version Control

#### Commit Messages
- Imperative mood: "Add feature" not "Added feature"
- Subject line < 50 characters
- Body for detailed explanation
- Reference issues when applicable

```
Add user authentication to task views

- Add @login_required decorator to all task views
- Filter tasks by current user
- Add logout functionality
```

#### Branch Naming
- `feature/description` - New features
- `fix/description` - Bug fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation changes

#### .gitignore Patterns
- Virtual environment: `myvenv/`, `venv/`
- Python cache: `__pycache__/`, `*.pyc`
- Database: `db.sqlite3` (development)
- Media files: `media/` (user uploads)
- Log files: `*.log`

## Django Configuration

### Settings (todo/settings.py)
- **DEBUG**: `True` dev, `False` prod
- **SECRET_KEY**: Environment variable in production
- **DATABASES**: SQLite dev, PostgreSQL recommended prod
- **INSTALLED_APPS**: Includes `tasks` app, `django.contrib.auth`, `django.contrib.sessions`
- **MEDIA_URL/MEDIA_ROOT**: `/media/` and `BASE_DIR / 'media'`
- **LOGIN_URL**: `'login'`
- **LOGIN_REDIRECT_URL**: `'list'`
- **LOGOUT_REDIRECT_URL**: `'login'`

### URL Configuration
- Root: `/` → `tasks.urls`
- Admin: `/admin/`
- API endpoints:
  - `GET /api/tasks/` - List tasks
  - `POST /api/tasks/create/` - Create task
  - `POST /api/tasks/<id>/update/` - Update task
  - `POST /api/tasks/<id>/delete/` - Delete task
  - `POST /api/tasks/<id>/toggle/` - Toggle completion

### Models
- **Task**: User, title, description, image, completion status, created_at
- **TaskImage**: Multiple images per task with ordering

### Views
- **Authentication**: `login_view`, `register_view`, `logout_view`
- **API**: `api_get_list`, `api_task_create`, `api_task_update`, `api_task_delete`, `api_task_toggle`
- **Pages**: `list` (main page)

## Common Tasks

### Add New Model Field
1. Edit `tasks/models.py`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. Update views if needed

### Add New API Endpoint
1. Add view function in `tasks/views.py`
2. Add URL pattern in `tasks/urls.py`
3. Update Vue.js frontend to call endpoint
4. Add tests in `tasks/tests.py`

### Fix a Bug
1. Identify issue (check `.cursor/debug.log` for logs)
2. Write failing test that reproduces bug
3. Fix the code
4. Run tests to verify
5. Commit with descriptive message

### Add Tests
```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from tasks.models import Task

class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test123')
    
    def test_task_list_view(self):
        self.client.login(username='test', password='test123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
```

## Production Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure proper database (PostgreSQL)
- [ ] Set `SECRET_KEY` from environment variable
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Use production web server (Gunicorn + Nginx)
- [ ] Set up SSL/HTTPS
- [ ] Configure file storage (S3 for media files)
- [ ] Set up monitoring and error tracking
- [ ] Backup database regularly

## Debugging

### Django Debugging
- Check `.cursor/debug.log` for detailed logs
- Use Django debug page (when `DEBUG=True`)
- Django shell: `python manage.py shell`
- Database shell: `python manage.py dbshell`

### Vue.js Debugging
- Browser console (F12)
- Network tab for API calls
- Vue DevTools browser extension

### Common Issues
- **CSRF errors**: Ensure CSRF token included in fetch requests
- **404 errors**: Check URL patterns in `tasks/urls.py`
- **Permission errors**: Add `@login_required` decorator
- **Image upload fails**: Check file size limits and MIME types

## Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd django-vue-todo-app

# Activate virtual environment
source myvenv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Resources

- Django Documentation: https://docs.djangoproject.com/
- Vue.js 3 Documentation: https://vuejs.org/
- Bootstrap 5 Documentation: https://getbootstrap.com/docs/5.3/
- Django REST Framework: https://www.django-rest-framework.org/

---

**Last Updated:** 2026-01-17
**Django Version:** 6.0.1
**Vue.js Version:** 3.x (CDN)
**Database:** SQLite (development)
