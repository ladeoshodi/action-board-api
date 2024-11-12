from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from .models import TaskList
from .serializers.common import TaskListSerializer
from .serializers.populated import PopulatedTaskListSerializer

from drf_spectacular.utils import extend_schema


class TaskListView (APIView):
    permission_classes = IsAuthenticated,


class TaskListListView(TaskListView):

    @extend_schema(
        tags=["TaskList"],
        responses=PopulatedTaskListSerializer,
    )
    def get(self, request):
        task_lists = TaskList.objects.all().filter(user=request.user.id)
        serialized_task_lists = PopulatedTaskListSerializer(
            task_lists, many=True)
        return Response(serialized_task_lists.data)

    @extend_schema(
        tags=["TaskList"],
        request=TaskListSerializer,
        responses={201: TaskListSerializer}
    )
    def post(self, request):
        request.data["user"] = request.user.id
        task_list_to_add = TaskListSerializer(data=request.data)
        try:
            task_list_to_add.is_valid(raise_exception=True)
            task_list_to_add.save()
            return Response(task_list_to_add.data, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(task_list_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TaskListDetailView(TaskListView):

    def get_task_list(self, user, pk):
        try:
            return TaskList.objects.get(user=user, pk=pk)
        except TaskList.DoesNotExist:
            raise NotFound(detail="TaskList not found")

    @extend_schema(
        tags=["TaskList"],
        responses=PopulatedTaskListSerializer
    )
    def get(self, request, pk):
        task_list = self.get_task_list(user=request.user.id, pk=pk)
        serialized_task_list = PopulatedTaskListSerializer(task_list)
        return Response(serialized_task_list.data)

    @extend_schema(
        tags=["TaskList"],
        request=TaskListSerializer,
        responses=TaskListSerializer
    )
    def put(self, request, pk):
        request.data["user"] = request.user.id
        task_list_to_update = self.get_task_list(user=request.user.id, pk=pk)
        updated_task_list = TaskListSerializer(
            task_list_to_update, data=request.data, partial=True)
        try:
            updated_task_list.is_valid(raise_exception=True)
            updated_task_list.save()
            return Response(updated_task_list.data, status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return Response(updated_task_list.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @extend_schema(
        tags=["TaskList"]
    )
    def delete(self, request, pk):
        task_list_to_delete = self.get_task_list(user=request.user.id, pk=pk)
        task_list_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
