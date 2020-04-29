from django.urls import path

from . import views

urlpatterns = [
    path('add-facility-to-list/', views.add_facility_to_list,
         name='add-facility-to-list'),

    path('', views.warehouse, name='warehouse'),
]
