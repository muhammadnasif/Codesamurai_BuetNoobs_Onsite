from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import observer.views as observer_views
import observer.authentication_module as observer_au

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # path('', observer_views.load, ''),
                  path('', include('observer.urls', namespace='observer')),
                  path('login/', observer_au.log_in, name='login'),
                  path('logout/', observer_au.logout_request, name='logout'),
                  path('registration/', observer_au.registration, name='register'),
                  path('project-proposal/', observer_views.project_proposal, name='project_proposal'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
