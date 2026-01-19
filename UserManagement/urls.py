from django.contrib import admin
from django.urls import path,include
from UserManagement.views import AddSystemUser,DeleteUser,EditUser,ViewSystemUser

urlpatterns = [
    path('ViewSystemUser',ViewSystemUser,name='ViewSystemUser'),
    path('AddSystemUser',AddSystemUser,name='AddSystemUser'),
    # EditUser
    path('EditUser/<int:id>',EditUser,name='EditUser'),
    # DeleteUser
    path('DeleteUser/<int:id>',DeleteUser,name='DeleteUser'),

]
