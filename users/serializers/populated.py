from django.contrib.auth import get_user_model

from tasklists.serializers.common import TaskListSerializer
from tasks.serializers.common import TaskSerializer
from tags.serializers.common import TagSerializer

from .common import BaseUserSerializer

User = get_user_model()


class PopulatedUserSerializer(BaseUserSerializer):
    lists = TaskListSerializer(many=True)
    tasks = TaskSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("lists", "tasks", "tags")
