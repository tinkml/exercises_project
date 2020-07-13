from django.contrib import admin
from .models import TasksCategory, Tasks, UsersCategoryLevel


admin.site.register((TasksCategory, Tasks, UsersCategoryLevel))
