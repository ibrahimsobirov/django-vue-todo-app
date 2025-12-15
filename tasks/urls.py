from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
]



urlpatterns += [
    path('api/tasks/', views.api_get_list, name='api_get_list'),
    path('api/tasks/create/', views.api_task_create, name='api_task_create'),
]