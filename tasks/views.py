from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from .models import Task
from .serializers.common import TaskSerializer
from .serializers.populated import PopulatedTaskSerializer

from drf_spectacular.utils import extend_schema


class TaskView (APIView):
    permission_classes = IsAuthenticated,


class TaskListView(TaskView):

    @extend_schema(
        tags=["Task"],
        responses=PopulatedTaskSerializer,
    )
    def get(self, request):
        tasks = Task.objects.all().filter(user=request.user.id)
        serialized_tasks = PopulatedTaskSerializer(
            tasks, many=True)
        return Response(serialized_tasks.data)

    @extend_schema(
        tags=["Task"],
        request=TaskSerializer,
        responses={201: TaskSerializer}
    )
    def post(self, request):
        request.data["user"] = request.user.id
        task_list_to_add = TaskSerializer(data=request.data)
        try:
            task_list_to_add.is_valid(raise_exception=True)
            task_list_to_add.save()
            return Response(task_list_to_add.data, status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(task_list_to_add.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TaskDetailView(TaskView):

    def get_task(self, user, pk):
        try:
            return Task.objects.get(user=user, pk=pk)
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found")

    @extend_schema(
        tags=["Task"],
        responses=PopulatedTaskSerializer
    )
    def get(self, request, pk):
        task_list = self.get_task(user=request.user.id, pk=pk)
        serialized_task_list = PopulatedTaskSerializer(task_list)
        return Response(serialized_task_list.data)

    @extend_schema(
        tags=["Task"],
        request=TaskSerializer,
        responses=TaskSerializer
    )
    def put(self, request, pk):
        request.data["user"] = request.user.id
        task_to_update = self.get_task(user=request.user.id, pk=pk)
        updated_task = TaskSerializer(
            task_to_update, data=request.data, partial=True)
        try:
            updated_task.is_valid(raise_exception=True)
            updated_task.save()
            return Response(updated_task.data, status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return Response(updated_task.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e.__dict__ if e.__dict__ else str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @extend_schema(
        tags=["Task"]
    )
    def delete(self, request, pk):
        task_to_delete = self.get_task(user=request.user.id, pk=pk)
        task_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
