from django.contrib import admin
from django.urls import path,include
from student.views import ViewStudent,UpdateStudent,DeleteStudent,DataManagementStudent

urlpatterns = [
            # datamanagement 
          #student
    path('AddStudent',DataManagementStudent,name='DataManagementStudent'),
                #view students
    path('ViewStudent',ViewStudent,name="ViewStudent"),
                #update students 
    path('UpdateStudent/<int:id>',UpdateStudent,name="UpdateStudent"),
  
                #delete Students
    path('DeleteStudent/<int:id>',DeleteStudent,name='DeleteStudent'),

]