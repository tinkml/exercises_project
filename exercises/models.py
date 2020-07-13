from django.db import models
from django.contrib.auth.models import User


class TasksCategory(models.Model):
    """Categories for tasks"""
    name = models.CharField(max_length=100)
    url = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tasks(models.Model):
    """Tasks for users to solve"""
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    level = models.PositiveIntegerField(blank=True, null=True)
    category = models.ForeignKey(TasksCategory, on_delete=models.CASCADE)
    url = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class UsersCategoryLevel(models.Model):
    """M2M. It keeps user's progress in every category"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(TasksCategory, on_delete=models.CASCADE)
    solved_tasks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'User''s  category level'
        verbose_name_plural = 'User''s categories level'
