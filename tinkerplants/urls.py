from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_display', views.update_display, name='update_display'),
    path('update_imps', views.update_implants, name='update_imps'),
    path('update_ql', views.update_ql, name='update_ql')
]