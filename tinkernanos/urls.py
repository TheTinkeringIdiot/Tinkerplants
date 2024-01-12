from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_stats', views.update_stats, name='update_stats'),
]