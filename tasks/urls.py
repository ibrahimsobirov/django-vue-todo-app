from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
]

urlpatterns += [
    path('api/tasks/', views.api_get_list, name='api_get_list'),
    path('api/tasks/create/', views.api_task_create, name='api_task_create'),
    path('api/tasks/<int:task_id>/update/', views.api_task_update, name='api_task_update'),
    path('api/tasks/<int:task_id>/delete/', views.api_task_delete, name='api_task_delete'),
    path('api/tasks/<int:task_id>/toggle/', views.api_task_toggle, name='api_task_toggle'),
]