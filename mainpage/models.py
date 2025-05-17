from django.db import models

class TodoList(models.Model):
    task = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - {'Done' if self.is_checked else 'Pending'}"