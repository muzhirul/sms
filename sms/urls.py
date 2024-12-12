"""
URL configuration for sms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = 'School Management System'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('securelogin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('academic/',include('academic.urls')),
    path('student/',include('student.urls')),
    path('staff/',include('staff.urls')),
    path('setup/',include('setup_app.urls')),
    path('exam/',include('exam.urls')),
    path('hrms/',include('hrms.urls')),
    path('fees/',include('fees.urls')),
    path('communicate/',include('communicate.urls')),
    path('account/',include('account.urls')),
    path('inventory/',include('inventory.urls')),
    path('purchase/',include('purchase.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
