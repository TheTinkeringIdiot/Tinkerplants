from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_display', views.update_display, name='update_display'),
    path('update_imps', views.update_implants, name='update_imps'),
    path('update_ql', views.update_ql, name='update_ql'),
    path('update_all_ql', views.update_all_ql, name='update_all_ql'),
    path('save_profile', views.save_profile, name='save_profile'),
    path('load_profile', views.load_profile, name='load_profile'),
    path('construct_imp', views.construct_imp, name='construct_imp')
]