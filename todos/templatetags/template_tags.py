from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def task_time_left(task):
    now = timezone.now()
    time_left = task.deadline - now
    days = time_left.days
    hours = time_left.seconds // 3600
    mins = (time_left.seconds % 3600) // 60
    if days<0:
        return f'این تسک {days * -1} روز پیش منقضی شد'
    return f"{days}روز و {hours}ساعت و {mins} دقیقه"
