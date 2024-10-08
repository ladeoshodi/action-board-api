from django.urls import path
from .views import TaskListListView, TaskListDetailView

urlpatterns = [
    path('', TaskListListView.as_view()),
    path('<int:pk>/', TaskListDetailView.as_view())
]
