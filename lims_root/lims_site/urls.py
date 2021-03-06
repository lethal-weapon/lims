"""lims_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('bulletin/', include('bulletin.urls')),
    path('inventory/', include('inventory.urls')),
    path('application/', include('applications.urls')),

    path('tips/', TemplateView.as_view(template_name='lims_site/tips.html'), name='site-tips'),
    path('', TemplateView.as_view(template_name='lims_site/index.html'), name='index'),
]

# Django Admin Settings
admin.site.site_header = "LIMS Admin"
admin.site.site_title = "LIMS Admin Portal"
admin.site.index_title = "Welcome to LIMS"
