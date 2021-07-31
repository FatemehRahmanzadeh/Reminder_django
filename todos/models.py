from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from todos.managers import TaskManager, CategoryManager


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_categories')
    objects = CategoryManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name='unique_group')
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_tasks_list', args=[str(self.id)])


class Task(models.Model):
    PRIORITY = [
        ('1', 'مهم و فوری'),  # الان انجامش بده
        ('2', 'غیرمهم و فوری'),  # بسپار به دیگری یا یه وقتی براش خالی کن
        ('3', 'مهم و غیرفوری'),  # براش برنامه ریزی کن
        ('4', 'غیرمهم و غیرفوری'),  # ترجیحاٌ حذفش کن یا بذار برای تعطیلات
    ]
    STATUS = [('U', 'ناتمام'), ('D', 'انجام شد')]
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=720, blank=True, default='')
    category = models.ManyToManyField(Category, related_name='category', related_query_name='cat_tasks')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=2, choices=PRIORITY)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=1, default='U', choices=STATUS)
    objects = TaskManager()

    class Meta:
        ordering = ['deadline']
        constraints = [
            models.UniqueConstraint(fields=['title', 'user'], name='unique_group_task')
        ]

    def __str__(self):
        return f'"{self.title}" ({self.id}) task, deadline:{self.deadline}'

    def get_absolute_url(self):
        """
         از آنجا که در آدرس یو آر ال یک پرایمری کی برای دسترسی به آبجکت وارد می کنیم،
          این متد براساس آیدی هر آبجکت یک یو آر ال یکتا ایجاد می کند که دسترسی به آن را در دیتابیس فراهم می کند.

        :return: یک یوآر ال یکتا به ازای هر آبجکت
        """
        return reverse('details', args=[str(self.id)])

    def as_dict(self):
        return {
            "id": self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'deadline': self.deadline,
            'status': self.status,
        }
