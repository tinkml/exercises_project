from django.contrib import admin
from .models import Category, Task, UsersCategoryLevel


admin.site.register((Category, Task, UsersCategoryLevel))
