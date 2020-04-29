from django.urls import path

from . import views

urlpatterns = [
    path('my-list/', views.my_list, name='my-list'),
    path('apply-facility/', views.apply_facility, name='apply-facility'),
    path('apply-research/', views.apply_research, name='apply-research'),

    path('update-facility/', views.update_facility_application,
         name='update-facility-application'),
    path('delete-facility/', views.delete_facility_application,
         name='delete-facility-application'),
]
