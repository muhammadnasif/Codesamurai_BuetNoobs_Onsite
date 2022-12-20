from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import observer.views as observer_views

app_name = 'observer'

urlpatterns = [
    path('api/projects/', observer_views.projects, name='projects'),
    path('api/projects/filter', observer_views.filter_projects, name='filter_projects'),
    path('project', observer_views.project, name='project'),
    path('', observer_views.load, name='home'),
    path('issue/<int:pk>/', observer_views.post_issue, name='post_issue')
]
