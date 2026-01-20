from django.urls import path
from analytic.views import studentpercourse,MonthlyRevenue,ActiveStudent,analytics_enrollment_trends
urlpatterns = [
    
# --------Analytics----------#
# studentpercourse
    path('AdminDashboard/Analytics/studentpercourse',studentpercourse,name="studentpercourse"),
#  MonthlyReveneu

    path('AdminDashboard/Analytics/MonthlyRevenue',MonthlyRevenue,name="MonthlyRevenue"),
    # ActiveStudent

    path('AdminDashboard/Analytics/ActiveStudent',ActiveStudent,name="ActiveStudent"),
    # analytics_enrollment_trends
    path('AdminDashboard/Analytics/analytics_enrollment_trends',analytics_enrollment_trends,name="analytics_enrollment_trends"),

]
