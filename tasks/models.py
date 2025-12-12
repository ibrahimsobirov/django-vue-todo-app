from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        # Displays the task title in the Django Admin
        return self.title

    class Meta:
        # Orders tasks by creation date (newest first)
        ordering = ['-created_at']