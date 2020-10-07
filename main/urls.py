"""flemmer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('update_details', views.update_details, name='update_details'),
    path('get_details', views.get_details, name='get_details'),
    path('set_plan_civilian', views.set_plan_civilian, name='set_plan_civilian'),
    path('get_all_plans', views.get_all_plans, name='get_all_plans'),
    path('start_or_stop_beeep', views.start_or_stop_beeep, name='start_or_stop_beeep'),
    path('ping_lawyer', views.ping_lawyer, name='ping_lawyer'),
    path('get_all_beeps', views.get_all_beeps, name='get_all_beeps'),
    path('add_buddy', views.add_buddy, name='add_buddy'),
    path('add_location', views.add_location, name='add_location'),
    path('get_user_location/<str:phone>', views.get_user_location, name='get_user_location'),
    path('get_closest_lawyers', views.get_closest_lawyers, name='get_closest_lawyers'),
    path('get_closest_lawyers_to_user/<str:phone>', views.get_closest_lawyers_to_user, name='get_closest_lawyers_to_user'),
    path('get_all_forms/', views.get_all_forms, name='get_all_forms'),
    path('post_credentials_form/', views.post_credentials_form, name='post_credentials_form')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)