"""
URL configuration for Site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import index, generate_random_variant, show_vars, show_variant, show_task, solve_variant


urlpatterns = [
    path('', index, name='home'),
    path('gen-r-var/cat-<str:cat_name>/diff-<int:difficulty>/answers-<str:answers>/', generate_random_variant, name='gen-r-var'),
    path('show-vars/cat-<str:cat_name>/', show_vars, name='show-vars'),
    path('show-vars/cat-<str:cat_name>/page-<int:page>/', show_vars, name='show-vars'),
    path('show-variant/cat-<str:cat_name>/id-<int:var_id>/answers-<str:answers>', show_variant, name='show-variant'),
    path('show-task/id-<int:task_id>/', show_task, name='show-task'),
    path('solve-variant/cat-<str:cat_name>/id-<int:var_id>/task-<int:task_number>/', solve_variant, name='solve-variant'),
]
