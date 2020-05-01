from django.urls import path

from . import views

urlpatterns = [
    path('my-list/', views.my_list, name='my-list'),

    path('cfa/', views.create_facility_application,
         name='create-facility-application'),
    path('ajax-fa/', views.ajax_fa_switcher,
         name='ajax-fa'),
    path('ajax-rffl', views.remove_facility_from_list,
         name='remove-facility-from-list'),


    path('cra/', views.create_research_application,
         name='create-research-application'),

]
