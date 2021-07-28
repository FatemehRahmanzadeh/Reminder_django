from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('task/create', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', TaskDetailView.as_view(), name='details'),
    path('<int:pk>/', TaskUpdateView.as_view(), name='edit_task'),
    path('<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='ctg_create'),
    path('<int:pk>/', CategoryUpdateView.as_view(), name='edit_ctg'),
    path('<int:pk>/', CategoryTasksListView.as_view(), name='category_tasks_list'),
    path('<int:pk>/', DeleteCategoryView.as_view(), name='delete_ctg'),
]
