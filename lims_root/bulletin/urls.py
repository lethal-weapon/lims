from django.urls import path

from . import views

urlpatterns = [
    path('news/', views.site_news, name='site-news'),
]
