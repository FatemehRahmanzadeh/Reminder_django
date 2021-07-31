# Generated by Django 3.2.5 on 2021-07-31 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_alter_task_priority'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='task',
            constraint=models.UniqueConstraint(fields=('title', 'user'), name='unique_group_task'),
        ),
    ]
