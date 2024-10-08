from users.serializers.common import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from .common import TagSerializer


class PopulatedTagSerializer(TagSerializer):
    user = UserSerializer()
