from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('tasks/json/', json_tasks, name='tasks_json'),
    path('task/create', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/detail/', TaskDetailView.as_view(), name='details'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='edit_task'),
    path('task/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='ctg_create'),
    path('category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='edit_ctg'),
    path('<int:pk>/detail/', CategoryTasksListView.as_view(), name='category_tasks_list'),
    path('<int:pk>/delete/', DeleteCategoryView.as_view(), name='delete_ctg'),
]
