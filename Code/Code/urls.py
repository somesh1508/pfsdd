from django.contrib import admin
from django.urls import path, include
from codeeditor import views
from codeeditor.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # This routes the root URL to the home view
    path('codeeditor/', include('codeeditor.urls')),  # This will include all URLs from codeeditor app
    path('accounts/', include('django.contrib.auth.urls')),  # For login, logout, password management
    ]
