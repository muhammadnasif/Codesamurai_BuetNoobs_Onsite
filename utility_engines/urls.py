from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import utility_engines.views as utility_views

app_name = 'utility'

urlpatterns = [
    path('suggest/<int:pk>/', utility_views.suggest_query, name='suggest_query'),
]
