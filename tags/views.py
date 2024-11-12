from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from .models import Tag
from .serializers.common import TagSerializer
from .serializers.populated import PopulatedTagSerializer

from drf_spectacular.utils import extend_schema


class TagView (APIView):
    permission_classes = IsAuthenticated,


class TagListView(TagView):

    @extend_schema(
        tags=["Tag"],
        responses=PopulatedTagSerializer,
    )
    def get(self, request):
        tags = Tag.objects.all().filter(user=request.user.id)
        serialized_tags = PopulatedTagSerializer(tags, many=True)
        return Response(serialized_tags.data)

    @extend_schema(
        tags=["Tag"],
        request=TagSerializer,
        responses={201: TagSerializer}
    )
    def post(self, request):
        request.data["user"] = request.user.id
        tag_to_add = TagSerializer(data=request.data)
        try:
            tag_to_add.is_valid(raise_exception=True)
            tag_to_add.save()
            return Response(tag_to_add.data, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(tag_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TagDetailView(TagView):

    def get_tag(self, user, pk):
        try:
            return Tag.objects.get(user=user, pk=pk)
        except Tag.DoesNotExist:
            raise NotFound(detail="Tag not found")

    @extend_schema(
        tags=["Tag"],
        responses=PopulatedTagSerializer
    )
    def get(self, request, pk):
        tag = self.get_tag(user=request.user.id, pk=pk)
        serialized_tag = PopulatedTagSerializer(tag)
        return Response(serialized_tag.data)

    @extend_schema(
        tags=["Tag"]
    )
    def delete(self, request, pk):
        tag_to_delete = self.get_tag(user=request.user.id, pk=pk)
        tag_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
