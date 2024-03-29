"""rental03 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('profile/', user_view.profile, name='user-profile'),
    path('agent/', user_view.agent, name='user-agent'),
    path('landlord/update/', user_view.landlord_update, name='user-landlord-update'),
    path('agent/update/', user_view.agent_update, name='user-agent-update'),
    
    path('tenant/update/<int:pk>/', user_view.tenant_update, name='user-tenant-update'),
    path('tenant/delete/<int:pk>/', user_view.tenant_delete, name='user-tenant-delete'),
    path('agent/delete/<int:pk>/', user_view.agent_delete, name='user-agent-delete'),
    path('change/password/<int:pk>/', user_view.change_password, name='user-change-password'),
    path('', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)