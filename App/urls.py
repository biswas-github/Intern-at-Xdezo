from django.urls import path,include
from . views import LoginPage,AdminDashboard,ViewerDashboard,Downloads,Signup
from . views import download_report

# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    # Signup
    path('Signup/',Signup,name='Signup'),


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
