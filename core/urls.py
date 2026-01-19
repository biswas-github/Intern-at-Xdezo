
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    # Usermanagement
    path('AdminDashboard/UserManagement/',include('UserManagement.urls')),
    # student
    path('AdminDashboard/DataManagementStudent/',include('student.urls')),



]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
