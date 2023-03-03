from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('boss_info', views.boss_info, name='boss_info'),
    path('filter', views.filter, name='filter'),
    path('match', views.match, name='match'),
    path('compare', views.compare, name='compare'),
    # path('update_display', views.update_display, name='update_display'),
    # path('save_stats', views.save_stats, name='save_stats'),
    # path('restore_stats', views.restore_stats, name='restore_stats')
]