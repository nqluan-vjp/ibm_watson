from django.urls import path

from . import views

urlpatterns = [
    path('', views.search_data, name='search'),
    path('search', views.search_data, name='search'),
    path('trending', views.trending_topic, name='trending'),
    path('export', views.export_csv, name='export'),
]