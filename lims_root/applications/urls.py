from django.urls import path

from . import views

urlpatterns = [
    path('my-list/', views.my_list, name='my-list'),
    path('apply-facility/', views.apply_facility, name='apply-facility'),
    path('apply-research/', views.apply_research, name='apply-research'),

]
