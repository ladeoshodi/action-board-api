from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        "users.User", related_name="tags", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
