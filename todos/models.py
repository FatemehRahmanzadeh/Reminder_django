from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('categories', args=[str(self.id)])


class Task(models.Model):
    PRIORITY = [
        ('1', 'urgent & important'),  # الان انجامش بده
        ('2', 'urgent & unimportant'),  # بسپار به دیگری یا یه وقتی براش خالی کن
        ('3', 'not urgent & important'),  # براش برنامه ریزی کن
        ('4', 'not urgent & unimportant'),  # ترجیحاٌ حذفش کن یا بذار برای تعطیلات
    ]
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=720, blank=True, default='')
    category = models.ManyToManyField(Category, related_name='category')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=2, choices=PRIORITY)
    deadline = models.DateTimeField()

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return f'"{self.title}" ({self.id}) task, deadline:{self.deadline}'

    def get_absolute_url(self):
        """
         از آنجا که در آدرس یو آر ال یک پرایمری کی برای دسترسی به آبجکت وارد می کنیم،
          این متد براساس آیدی هر آبجکت یک یو آر ال یکتا ایجاد می کند که دسترسی به آن را در دیتابیس فراهم می کند.

        :return: یک یوآر ال یکتا به ازای هر آبجکت
        """
        return reverse('details', args=[str(self.id)])
