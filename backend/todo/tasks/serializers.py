from rest_framework import serializers
from .models import Task 

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id', 
            'title', 
            'created_by', 
            'description', 
            'created_at', 
            'deadline',
            'completed_at'
        )
        read_only_fields = ('created_at',)