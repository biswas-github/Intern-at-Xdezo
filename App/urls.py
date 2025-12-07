from django.urls import path,include
from . views import LoginPage,AdminDashboard,ViewerDashboard,DataManagementStudent


# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    path('',LoginPage,name='login'),
    # for admindashboard
    path('AdminDashboard/',AdminDashboard,name='AdminDashboard'),
        # datamanagement 
          #student
    path('AdminDashboard/DataManagementStudent',DataManagementStudent,name='DataManagementStudent'),
    # for viewer dashboard
    path('ViewerDashboard/',ViewerDashboard,name='ViewerDashboard')

]
