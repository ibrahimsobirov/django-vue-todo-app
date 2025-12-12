from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.task, name='create'),
    path('<int:task_id>/', views.detail, name='details'),
    path('<int:task_id>/edit/', views.edit, name='edit'),
    path('<int:task_id>/delete/', views.delete, name='delete'), 
]