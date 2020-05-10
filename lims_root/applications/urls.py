from django.urls import path

from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('my-list/', views.my_list, name='my-list'),

    path('cfa/', TemplateView.as_view(template_name='applications/apply-facility.html'),
         name='create-facility-application'),
    path('cra/', TemplateView.as_view(template_name='applications/apply-research.html'),
         name='create-research-application'),

    path('ajax-application-switcher/', views.ajax_application_switcher,
         name='ajax-application-switcher'),
    path('ajax-account-switcher/', views.ajax_account_switcher,
         name='ajax-account-switcher'),

    path('ajax-rffl', views.remove_facility_from_list,
         name='remove-facility-from-list'),
]
