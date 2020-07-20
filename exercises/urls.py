from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('categories', views.show_categories, name='categories'),
    path('none_task', views.none_task, name='none_task'),
    path('logout', views.log_out_user, name='logout'),
    path('task', views.get_task),
    path('<slug:category>/<slug:lvl>/<slug:task_url>/<slug:vars_str>', views.show_task_from_url),
]