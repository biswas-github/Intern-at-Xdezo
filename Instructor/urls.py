
from django.urls import path
from Instructor.views import Instructor1,AddInstructor,DeleteInstructor,UpdateInstructor

urlpatterns = [
    
    path('Instructor',Instructor1,name="Instructor"),
#               UpdateInstructor

    path('UpdateInstructor/<int:id>',UpdateInstructor,name="UpdateInstructor"),
                # DeleteInstructor
    path('DeleteInstructor/<int:id>',DeleteInstructor,name="DeleteInstructor"),
            # AddInstructor
    path('AddInstructor',AddInstructor,name="AddInstructor"),
]
