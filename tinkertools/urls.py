from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:id>/', views.item, name='item'),
    path('item/<int:id>/<int:ql>/', views.item, name='item'),
    path('search', views.search, name='search'),
    path("robots.txt",TemplateView.as_view(template_name="tinkertools/robots.txt", content_type="text/plain")),
    path("sitemap.xml",TemplateView.as_view(template_name="tinkertools/sitemap.xml", content_type="text/plain")),
]