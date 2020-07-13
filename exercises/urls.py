from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.show_categories),
    path('signup', views.sign_up_user, name='signup'),
    path('logout', views.log_out_user, name='logout'),
    path('login', views.log_in_user, name='login'),
    path('task', views.get_task),
    path('<slug:category>/<slug:lvl>/<slug:task_url>/<slug:vars_str>', views.show_task_from_url),
]