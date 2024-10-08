from rest_framework import serializers
from .models import Tag
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PopulatedTagSerializer(TagSerializer):
    user = UserSerializer()
