from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import observer.views as observer_views
import observer.review_proposal as review_view

app_name = 'observer'

urlpatterns = [
    path('api/projects/', observer_views.projects, name='projects'),
    path('api/all-projects/', observer_views.all_projects, name='all-projects'),
    path('api/projects/filter', observer_views.filter_projects, name='filter_projects'),
    path('', observer_views.load, name='home'),
    path('post_feedback/', observer_views.post_feedback, name='post_feedback'),
    path('project-proposal/', observer_views.project_proposal, name='project-proposal'),
    path('project-proposal/update-proposal/', observer_views.update_proposal, name='update-proposal'),
    path('add-rating/', observer_views.add_rating, name='add-rating'),
    path('review-project-proposal/', review_view.review_project_proposal, name='review-project-proposal'),
    path('running-project/', review_view.running_project, name='running-project'),

    path('export-data/',observer_views.export_data, name='export-data'),
    path('export-data-search/',observer_views.export_data_search, name='export-data-search'),
]
