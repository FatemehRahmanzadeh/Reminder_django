from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

from .models import Task, Category


class CreateTask(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'deadline']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreateTask, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Task.objects.filter(user=user)
    # category = Task.user.user_categories

    # def get_users_data(self, user):
    #     category = ModelMultipleChoiceField(
    #         queryset=Category.objects.filter(user=user),
    #         widget=CheckboxSelectMultiple
    #     )
    #     return category


class CreateCategory(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
