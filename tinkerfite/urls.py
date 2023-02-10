from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_stats', views.update_stats, name='update_stats'),
    path('update_display', views.update_display, name='update_display'),
    path('save_stats', views.save_stats, name='save_stats'),
    path('restore_stats', views.restore_stats, name='restore_stats')
]