from users.serializers.common import UserSerializer
from tasklists.serializers.common import TaskListSerializer
from tags.serializers.common import TagSerializer

from .common import TaskSerializer


class PopulatedTaskSerializer(TaskSerializer):
    user = UserSerializer()
    task_list = TaskListSerializer()
    tags = TagSerializer(many=True)
