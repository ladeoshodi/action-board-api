from rest_framework import serializers
from ..models import TaskList


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskList
        fields = '__all__'

    def validate(self, data):
        """Validate that the task list name is unique to the logged in User"""
        user = data.get('user')
        name = data.get('name')

        existing_task_list = TaskList.objects.all().filter(name=name, user=user.id)

        if existing_task_list:
            raise serializers.ValidationError(
                {"name": "Task List name already exists"})

        return data
