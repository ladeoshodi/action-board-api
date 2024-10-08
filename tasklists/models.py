from django.db import models
from django.core.exceptions import ValidationError


class TaskList(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        "users.User", related_name="lists", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = TaskList.objects.get(pk=self.pk)
            if original.user != self.user:
                raise ValidationError({"user": "user field is immutable"})

        super(TaskList, self).save(*args, **kwargs)
