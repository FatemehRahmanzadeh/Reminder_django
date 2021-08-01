from django import forms
from django.contrib.admin import widgets
from django.forms import ModelForm
from .models import Task, Category


class CreateTask(forms.Form):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'deadline']


class CreateCategory(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
