from django.urls import path
from .views import TagListView, TagDetailView

urlpatterns = [
    path('', TagListView.as_view()),
    path('<int:pk>/', TagDetailView.as_view())

]
