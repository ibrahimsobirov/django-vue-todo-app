from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.CharField(max_length=100, default='Anonymous')
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    completed_at = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return self.title