from django.urls import path
# url patterns 
from classroom.views import ViewClassroom,AddClassroom,UpdateClassroom,DeleteClassroom

urlpatterns = [
    #   #--------------ClassRoom------------#
                #ViewClassroom
    path('ViewClassroom',ViewClassroom,name="ViewClassroom"),
                
# add classroom
    path('AddClassroom',AddClassroom,name="AddClassroom"),
                #UpdateClassroom
    path('UpdateClassroom/<int:id>',UpdateClassroom,name="UpdateClassroom"),
    path('DeleteClassroom/<int:id>',DeleteClassroom,name="DeleteClassroom"),
]
