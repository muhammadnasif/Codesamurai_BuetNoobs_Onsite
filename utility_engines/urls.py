from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import utility_engines.views as utility_views

app_name = 'utility'

urlpatterns = [
    path('suggest/<int:pk>/', utility_views.suggest_query, name='suggest_query'),
    path('suggest/all', utility_views.suggest_all, name='suggest_all'),
    path('expected_ends/', utility_views.expected_ends_post, name='expected_ends_post')
]
