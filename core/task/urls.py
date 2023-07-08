from django.urls import re_path, path
from . import views

urlpatterns = [
    re_path(r"^$", views.TaskListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/',
         views.TaskDetailView.as_view(),
         name='task_detail'
         ),
    path('update/<int:pk>/',
         views.TaskUpdateView.as_view(),
         name='task_update'
         ),
]
