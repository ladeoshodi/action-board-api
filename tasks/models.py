from django.db import models
from django.core.exceptions import ValidationError


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    done = models.BooleanField(default=False)
    task_list = models.ForeignKey(
        "tasklists.TaskList", related_name="tasks", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "users.User", related_name="tasks", on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        "tags.Tag", related_name="tasks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user} | List: {self.task_list}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Task.objects.get(pk=self.pk)
            if original.user != self.user:
                raise ValidationError({"user": "user field is immutable"})

        super(Task, self).save(*args, **kwargs)
