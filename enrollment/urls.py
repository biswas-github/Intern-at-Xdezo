from django.urls import path,include
from enrollment.views import ViewEnrollment,AddEnrollment,UpdateEnrollment,DeleteEnrollment

urlpatterns = [
    # -------Enrollments-----------#
    # ViewEnrollment
    path('ViewEnrollment',ViewEnrollment,name="ViewEnrollment"),

                #AddEnrollment
    path('AddEnrollment',AddEnrollment,name="AddEnrollment"),
    # Update enrollment
    path('UpdateEnrollment/<int:id>',UpdateEnrollment,name="UpdateEnrollment"),
        #AddEnrollment
    
            # DeleteEnrollment

    path('DeleteEnrollment/<int:id>',DeleteEnrollment,name="DeleteEnrollment"),
]
