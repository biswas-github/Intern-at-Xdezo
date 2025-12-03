from django.urls import path,include
from . views import LoginPage,AdminDashboard


# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    path('',LoginPage,name='login'),
    path('AdminDashboard/',AdminDashboard,name='AdminDashboard')
]
