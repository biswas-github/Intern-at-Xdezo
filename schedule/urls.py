from django.contrib import admin
from django.urls import path,include
from schedule.views import ViewSchedule,AddSchedule,FreeRoom,DeleteSchedule,EditSchedule

urlpatterns = [
    # --------Schedule-----------#
# ViewSchedule
    path('ViewSchedule',ViewSchedule,name="ViewSchedule"),
# Delete-Schedule
    path('DeleteSchedule/<int:id>',DeleteSchedule,name="DeleteSchedule"),
# AddSchedule
    path('AddSchedule/',AddSchedule,name="AddSchedule"),
# FreeRoom
    path('FreeRoom/',FreeRoom,name="FreeRoom"),
 # EditSchedule
    path('EditSchedule/<int:id>',EditSchedule,name="EditSchedule"),
]