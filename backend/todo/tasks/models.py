from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    # Added field for tracking creator
    created_by = models.CharField(max_length=100, default='Anonymous')
    description = models.TextField(blank=True, null=True)

    # Date fields
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    # Updated field to track completion time (null if not complete)
    completed_at = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return self.title