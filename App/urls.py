from django.urls import path,include
from . views import LoginPage,AdminDashboard,ViewerDashboard,DataManagementStudent,ViewStudent,UpdateStudent,DeleteStudent,CourseRegister,ViewCourses,UpdateCourse,DeleteCourse,ShowCourse,Batch,ViewBatches,Instructor,DeleteBatch,UpdateBatch,UpdateInstructor,DeleteInstructor,AddInstructor,ViewClassroom,AddClassroom,UpdateClassroom,DeleteClassroom,ViewEnrollment,UpdateEnrollment,AddEnrollment,DeleteEnrollment,ViewPayment,AddPayment,UpdatePayment,DeletePayment,DuesAndOverDues,ViewSchedule,DeleteSchedule,AddSchedule,EditSchedule,FreeRoom,Downloads,studentpercourse,MonthlyRevenue,ActiveStudent,analytics_enrollment_trends,Signup
from .views import ViewSystemUser,AddSystemUser,EditUser,DeleteUser
from .views import AllActivities,ExportDetails
from . views import download_report

# url patterns for the app
urlpatterns = [
    path('login/',LoginPage,name='login'),
    # Signup
    path('Signup/',Signup,name='Signup'),


    path('',LoginPage,name='login'),
    # for admindashboard
    path('AdminDashboard/',AdminDashboard,name='AdminDashboard'),

    # -------System User management-------#
    # ViewSystemUser
    path('AdminDashboard/UserManagement/ViewSystemUser',ViewSystemUser,name='ViewSystemUser'),
    path('AdminDashboard/UserManagement/AddSystemUser',AddSystemUser,name='AddSystemUser'),
    # EditUser
    path('AdminDashboard/UserManagement/EditUser/<int:id>',EditUser,name='EditUser'),
    # DeleteUser
    path('AdminDashboard/UserManagement/DeleteUser/<int:id>',DeleteUser,name='DeleteUser'),






        # datamanagement 
          #student
    path('AdminDashboard/DataManagementStudent/AddStudent',DataManagementStudent,name='DataManagementStudent'),
                #view students
    path('AdminDashboard/DataManagementStudent/ViewStudent',ViewStudent,name="ViewStudent"),
                #update students 
    path('AdminDashboard/DataManagementStudent/UpdateStudent/<int:id>',UpdateStudent,name="UpdateStudent"),
  
                #delete Students
    path('AdminDashboard/DataManagementStudent/DeleteStudent/<int:id>',DeleteStudent,name='DeleteStudent'),

    # -----Courses------
    path('AdminDashboard/DataManagementCourse/AddCourse',CourseRegister,name="Course"),
            # ViewCourses
    path('AdminDashboard/DataManagementStudent/ViewCourses',ViewCourses,name="ViewCourses"),
            #update course
    path('AdminDashboard/DataManagementStudent/ViewCourses/UpdateCourse/<int:id>',UpdateCourse,name="UpdateCourse"),
            #delete Course
    path('AdminDashboard/DataManagementStudent/ViewCourses/DeleteCourse/<int:id>',DeleteCourse,name='DeleteCourse'),
            #show course
    path('AdminDashboard/DataManagementStudent/ViewCourses/ShowCourse/<int:id>',ShowCourse,name="ShowCourse"),


    # ----------Batch----------
    path('AdminDashboard/Batch',Batch,name="Batch"),
                  #view batch 
    path('AdminDashboard/Batch/ViewBatches',ViewBatches,name="ViewBatches"),
#                        DeleteBatch
    path('AdminDashboard/Batch/DeleteBatch/<int:id>',DeleteBatch,name="DeleteBatch"),
#                       update batch
    path('AdminDashboard/Batch/UpdateBatch/<int:id>',UpdateBatch,name="UpdateBatch"),





    #-------Instructor----------# 

    path('AdminDashboard/Instructor',Instructor,name="Instructor"),
#               UpdateInstructor

    path('AdminDashboard/Instructor/UpdateInstructor/<int:id>',UpdateInstructor,name="UpdateInstructor"),
                # DeleteInstructor
    path('AdminDashboard/Instructor/DeleteInstructor/<int:id>',DeleteInstructor,name="DeleteInstructor"),
            # AddInstructor
    path('AdminDashboard/Instructor/AddInstructor',AddInstructor,name="AddInstructor"),



#   #--------------ClassRoom------------#
                #ViewClassroom
    path('AdminDashboard/ClassRoom/ViewClassroom',ViewClassroom,name="ViewClassroom"),
                
# add classroom
    path('AdminDashboard/ClassRoom/AddClassroom',AddClassroom,name="AddClassroom"),
                #UpdateClassroom
    path('AdminDashboard/ClassRoom/UpdateClassroom/<int:id>',UpdateClassroom,name="UpdateClassroom"),
    path('AdminDashboard/ClassRoom/DeleteClassroom/<int:id>',DeleteClassroom,name="DeleteClassroom"),



    # -------Enrollments-----------#
    # ViewEnrollment
    path('AdminDashboard/Enrollment/ViewEnrollment',ViewEnrollment,name="ViewEnrollment"),

                #AddEnrollment
    path('AdminDashboard/Enrollment/AddEnrollment',AddEnrollment,name="AddEnrollment"),
    # Update enrollment
    path('AdminDashboard/Enrollment/UpdateEnrollment/<int:id>',UpdateEnrollment,name="UpdateEnrollment"),
        #AddEnrollment
    path('AdminDashboard/Enrollment/AddEnrollment',AddEnrollment,name="AddEnrollment"),
            # DeleteEnrollment

    path('AdminDashboard/Enrollment/DeleteEnrollment/<int:id>',DeleteEnrollment,name="DeleteEnrollment"),



# -------Finance---------#
    path('AdminDashboard/Finance/ViewPayment',ViewPayment,name="ViewPayment"),
    # AddPayment
    path('AdminDashboard/Finance/AddPayment',AddPayment,name="AddPayment"),
    # UpdatePayment
    path('AdminDashboard/Payment/UpdatePayment/<int:id>',UpdatePayment,name="UpdatePayment"),
    path('AdminDashboard/Payment/DeletePayment/<int:id>',DeletePayment,name="DeletePayment"),
    # Dues and overdues
    path('AdminDashboard/Payment/DuesAndOverDues',DuesAndOverDues,name="DuesAndOverDues"),

# --------Schedule-----------#
# ViewSchedule
    path('AdminDashboard/Schedule/ViewSchedule',ViewSchedule,name="ViewSchedule"),
# Delete-Schedule
    path('AdminDashboard/Schedule/DeleteSchedule/<int:id>',DeleteSchedule,name="DeleteSchedule"),
# AddSchedule
    path('AdminDashboard/Schedule/AddSchedule/',AddSchedule,name="AddSchedule"),
# FreeRoom
    path('AdminDashboard/Schedule/FreeRoom/',FreeRoom,name="FreeRoom"),
 # EditSchedule
    path('AdminDashboard/Schedule/EditSchedule/<int:id>',EditSchedule,name="EditSchedule"),







# --------Analytics----------#
# studentpercourse
    path('AdminDashboard/Analytics/studentpercourse',studentpercourse,name="studentpercourse"),
#  MonthlyReveneu

    path('AdminDashboard/Analytics/MonthlyRevenue',MonthlyRevenue,name="MonthlyRevenue"),
    # ActiveStudent

    path('AdminDashboard/Analytics/ActiveStudent',ActiveStudent,name="ActiveStudent"),
    # analytics_enrollment_trends
    path('AdminDashboard/Analytics/analytics_enrollment_trends',analytics_enrollment_trends,name="analytics_enrollment_trends"),




# ------------system logs --------------#
# AllActivities
    path('AdminDashboard/System-Logs/AllActivities',AllActivities,name="AllActivities"),
# Export-Details
    path('AdminDashboard/System-Logs/Export-Details',ExportDetails,name="Export-Details"),
#---------download files , download reports -------------#
    path('AdminDashboard/download',download_report,name="download_report"),


 


    # ---------for viewer dashboard--------
    path('ViewerDashboard/',ViewerDashboard,name='ViewerDashboard'),

    # ----Downloads--------#Exports
    path('AdminDashboard/Exports/Downloads/',Downloads,name="Downloads"),


]
