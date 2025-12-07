from django.urls import path,include
from . views import LoginPage,AdminDashboard,ViewerDashboard


# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    path('',LoginPage,name='login'),
    # for admindashboard
    path('AdminDashboard/',AdminDashboard,name='AdminDashboard'),
    # for viewer dashboard
    path('ViewerDashboard/',ViewerDashboard,name='ViewerDashboard')

]
