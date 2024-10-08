from rest_framework import serializers
from ..models import Tag


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
