
from django.contrib import admin
from django.urls import path,include
from course.views import CourseRegister,DeleteCourse,UpdateCourse,ViewCourses

urlpatterns = [
     # -----Courses------
    path('AddCourse',CourseRegister,name="Course"),
            # ViewCourses
    path('ViewCourses',ViewCourses,name="ViewCourses"),
            #update course
    path('UpdateCourse/<int:id>',UpdateCourse,name="UpdateCourse"),
            #delete Course
    path('DeleteCourse/<int:id>',DeleteCourse,name='DeleteCourse'),
            #show course
    

]