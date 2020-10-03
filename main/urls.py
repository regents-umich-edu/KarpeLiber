from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name=views.index.__name__),
]
