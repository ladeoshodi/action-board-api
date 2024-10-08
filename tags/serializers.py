from rest_framework import serializers
from .models import Tag
from users.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def validate(self, data):
        """Validate that the tag is unique to the logged in User"""
        user = data.get('user')
        name = data.get('name')

        existing_tag = Tag.objects.all().filter(name=name, user=user.id)

        if existing_tag:
            raise serializers.ValidationError(
                {"name": "Tag name should be unique"})

        return data


class PopulatedTagSerializer(TagSerializer):
    user = UserSerializer()
