from django.urls import path

from . import views

urlpatterns = [
    path('', views.warehouse, name='warehouse'),
]
