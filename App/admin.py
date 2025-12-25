
# Register your models here.
from django.contrib import admin
from App.models import Payments,Batch,Classroom,Course,Enrollment,Schedule,Student,Instructor

# Register your models here.
admin.site.register(Student)
admin.site.register(Payments)
admin.site.register(Batch)
admin.site.register(Classroom)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Schedule)
admin.site.register(Instructor)

