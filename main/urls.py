from django.urls import path

from . import views
from .admin import ModelAdminIndexFormatter


urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('admin/main/volume/<int:volumeId>/download-index-print/', ModelAdminIndexFormatter.download_index_print, name='download-index-print'),
]
