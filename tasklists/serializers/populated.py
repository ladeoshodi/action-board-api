from users.serializers.common import UserSerializer
from .common import TaskListSerializer


class PopulatedTaskListSerializer(TaskListSerializer):
    user = UserSerializer()
