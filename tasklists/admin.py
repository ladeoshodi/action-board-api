from django.contrib import admin
from .models import TaskList

# Register your models here.


class TaskListAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(TaskList, TaskListAdmin)
