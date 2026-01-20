
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App.urls')),
    # Usermanagement
    path('AdminDashboard/UserManagement/',include('UserManagement.urls')),
    # student
    path('AdminDashboard/DataManagementStudent/',include('student.urls')),
    path('AdminDashboard/DataManagementCourse/',include('course.urls')),
    path('AdminDashboard/DataManagementBatch/',include('batch.urls')),
    path('AdminDashboard/DataManagementInstructor/',include('Instructor.urls')),
    path('AdminDashboard/DataManagementClassroom/',include('classroom.urls')),
    path('AdminDashboard/DataManagementEnrollment/',include('enrollment.urls')),
    path('AdminDashboard/Schedule/',include('schedule.urls')),
    path('AdminDashboard/payments/',include('payments.urls')),



]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
