from django.urls import path,include
from . views import LoginPage,AdminDashboard,ViewerDashboard,DataManagementStudent,ViewStudent,UpdateStudent,ShowStudent,DeleteStudent,Course,ViewCourses,UpdateCourse,DeleteCourse


# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    path('',LoginPage,name='login'),
    # for admindashboard
    path('AdminDashboard/',AdminDashboard,name='AdminDashboard'),
        # datamanagement 
          #student
    path('AdminDashboard/DataManagementStudent',DataManagementStudent,name='DataManagementStudent'),
                #view students
    path('AdminDashboard/DataManagementStudent/ViewStudent',ViewStudent,name="ViewStudent"),
                #update students 
    path('AdminDashboard/DataManagementStudent/UpdateStudent/<int:id>',UpdateStudent,name="UpdateStudent"),
                #show student
    path('AdminDashboard/DataManagementStudent/<int:id>',ShowStudent,name="ShowStudent"),
                #delete Students
    path('AdminDashboard/DataManagementStudent/DeleteStudent/<int:id>',DeleteStudent,name='DeleteStudent'),
    # -----Courses------
    path('AdminDashboard/Course',Course,name="Course"),
            # ViewCourses
    path('AdminDashboard/DataManagementStudent/ViewCourses',ViewCourses,name="ViewCourses"),
            #update course
    path('AdminDashboard/DataManagementStudent/ViewCourses/UpdateCourse/<int:id>',UpdateCourse,name="UpdateCourse"),
            #delete Course
    path('AdminDashboard/DataManagementStudent/ViewCourses/DeleteCourse/<int:id>',DeleteCourse,name='DeleteCourse'),





    # for viewer dashboard
    path('ViewerDashboard/',ViewerDashboard,name='ViewerDashboard'),
]
