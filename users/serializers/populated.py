from rest_framework import serializers
from django.contrib.auth import get_user_model

from tasklists.serializers.common import TaskListSerializer
from tasks.serializers.common import TaskSerializer
from tags.serializers.common import TagSerializer

User = get_user_model()


class PopulatedUserSerializer(serializers.ModelSerializer):
    lists = TaskListSerializer(many=True)
    tasks = TaskSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name",
                  "last_name", "profile_img", "lists", "tasks", "tags")
