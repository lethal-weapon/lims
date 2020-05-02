from django.urls import path

from . import views

urlpatterns = [
    path('my-list/', views.my_list, name='my-list'),

    path('cfa/', views.create_fa,
         name='create-facility-application'),
    path('cra/', views.create_ra,
         name='create-research-application'),

    path('ajax-fa/', views.ajax_fa_switcher,
         name='ajax-fa'),
    path('ajax-rffl', views.remove_facility_from_list,
         name='remove-facility-from-list'),

]
