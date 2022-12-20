"""Code_Samurai_Hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
                  path('login', observer_au.log_in, name='login'),
                  path('logout', observer_au.logout_request, name='logout')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
