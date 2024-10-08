from users.serializers.common import UserSerializer
from .common import TagSerializer


class PopulatedTagSerializer(TagSerializer):
    user = UserSerializer()
