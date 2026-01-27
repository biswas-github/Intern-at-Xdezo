from django.urls import path,include
from . views import LoginPage,AdminDashboard,ViewerDashboard,Downloads,Signup
from . views import download_report,Classroom_schedule_today

# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    # Signup
    path('Signup/',Signup,name='Signup'),

    # Classroom_schedule_today
    path('Classroom_schedule_today/',Classroom_schedule_today,name='Classroom_schedule_today'),



    path('',LoginPage,name='login'),
    # for admindashboard
    path('AdminDashboard/',AdminDashboard,name='AdminDashboard'),

#---------download files , download reports -------------#
    path('AdminDashboard/download',download_report,name="download_report"),

    # ---------for viewer dashboard--------
    path('ViewerDashboard/',ViewerDashboard,name='ViewerDashboard'),

    # ----Downloads--------#Exports
    path('AdminDashboard/Exports/Downloads/',Downloads,name="Downloads"),
    

]
