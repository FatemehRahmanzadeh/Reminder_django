from django.db import models
from django.utils import timezone


class TaskManager(models.Manager):
    def get_ex_tasks(self):
        return self.filter(deadline__lt=timezone.now())

    def get_early_tasks(self):
        return self.exclude(deadline__lt=timezone.now())

    def get_done_tasks(self):
        due = self.filter(status='U')
        done = self.exclude(status='U')
        return {'done': done, 'due': due}


class CategoryManager(models.Manager):
    def empty_categories(self):
        return self.filter(cat_tasks__isnull=True)

    def full_categories(self):
        return self.exclude(cat_tasks__isnull=True)
