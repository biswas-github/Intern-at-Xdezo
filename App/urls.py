from django.urls import path,include
from . views import LoginPage,AdminDashboard,ViewerDashboard,Downloads,studentpercourse,MonthlyRevenue,ActiveStudent,analytics_enrollment_trends,Signup

from .views import AllActivities,ExportDetails
from . views import download_report

# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    # Signup
    path('Signup/',Signup,name='Signup'),


    path('',LoginPage,name='login'),
    # for admindashboard
    path('AdminDashboard/',AdminDashboard,name='AdminDashboard'),






# --------Analytics----------#
# studentpercourse
    path('AdminDashboard/Analytics/studentpercourse',studentpercourse,name="studentpercourse"),
#  MonthlyReveneu

    path('AdminDashboard/Analytics/MonthlyRevenue',MonthlyRevenue,name="MonthlyRevenue"),
    # ActiveStudent

    path('AdminDashboard/Analytics/ActiveStudent',ActiveStudent,name="ActiveStudent"),
    # analytics_enrollment_trends
    path('AdminDashboard/Analytics/analytics_enrollment_trends',analytics_enrollment_trends,name="analytics_enrollment_trends"),




# ------------system logs --------------#
# AllActivities
    path('AdminDashboard/System-Logs/AllActivities',AllActivities,name="AllActivities"),
# Export-Details
    path('AdminDashboard/System-Logs/Export-Details',ExportDetails,name="Export-Details"),
#---------download files , download reports -------------#
    path('AdminDashboard/download',download_report,name="download_report"),


 


    # ---------for viewer dashboard--------
    path('ViewerDashboard/',ViewerDashboard,name='ViewerDashboard'),

    # ----Downloads--------#Exports
    path('AdminDashboard/Exports/Downloads/',Downloads,name="Downloads"),


]
