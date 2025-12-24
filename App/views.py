from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
def LoginPage(request):
    if request.method=='GET':
        print('get method')
        return render(request,'auth/login.html')
    if request.method=='POST':
        # if correct credential 
        username=request.POST.get('username') 
        password=request.POST.get('password') 
        print(f" username:{username } password:{password}")

        if username=='admin_demo' and password=="admin123":
            print("admin hit ")
            return redirect('AdminDashboard')
        elif username=='viewer_demo' and password=="viewer123":
            print("viewer  hit ")
            return redirect(request,'ViewerDashboard')

# admin dashboard after login 
def AdminDashboard(request):
    return render(request,'ADMIN/Admin-Dashboard.html')
# ----Students------#
# DataManagement-Student for managing the students 
def DataManagementStudent(request):
    return render(request,'ADMIN/DataManagement_Student.html')
# to view all the students
def ViewStudent(request):
    return render(request,'ADMIN/View-Student.html')
# updating the student
def UpdateStudent(request,id):
    return render(request,'ADMIN/Update-Student.html')
# showing the student details
def ShowStudent(request,id):
    return render(request,'ADMIN/Show-Student.html')
# delete the students
def DeleteStudent(request,id):
    return render(request,'ADMIN/Delete-Student.html')

# ----Courses------#
# DataManagement->courses for managing the Courses
def Course(request):
    return render(request,'ADMIN/Courses.html')
def ViewCourses(request):
    return render(request,'ADMIN/View-Courses.html')
def UpdateCourse(request,id):
    if request.method=="POST":
        # DO SOME LOGICS
        return redirect('ViewCourses')
    return render(request,'ADMIN/Update-Course.html')


def DeleteCourse(request,id):
    return render(request,'ADMIN/Delete-Course.html')
def ShowCourse(request,id):
    return render(request,'ADMIN/Show-Course.html')


# ----Batch------#
def Batch(request):
    return render(request,'ADMIN/Batch/Batch.html')

 #viewbatches
def ViewBatches(request):
    return render(request,'ADMIN/Batch/View-Batches.html')
# DeleteBatch
def DeleteBatch(request, id):
    return render(request,'ADMIN/BATCH/Delete-Batch.html')
# UpdateBatch
def UpdateBatch(request,id):
    return render(request,'ADMIN/BATCH/Update-Batch.html')

# -----Instructor-------
def Instructor(request):
    return render(request,'ADMIN/Instructor/View-Instructor.html')
# UpdateInstructor
def UpdateInstructor(request,id):
    return render(request,'ADMIN/Instructor/Update-Instructor.html')
# DeleteInstructor
def DeleteInstructor(request,id):
    return render(request,'ADMIN/Instructor/Delete-Instructor.html')
# AddInstructor
def AddInstructor(request):
    return render(request,'ADMIN/Instructor/Add-Instructor.html')

#------Classroom----#
# ViewClassroom
def ViewClassroom(request):
    return render(request,'ADMIN/Classroom/View-Classroom.html')
# addclassroom 
def AddClassroom(request):
     return render(request,'ADMIN/Classroom/Add-Classroom.html')
# update classroom
def UpdateClassroom(request,id):
     return render(request,'ADMIN/Classroom/Update-Classroom.html')
# DeleteClassroom
def DeleteClassroom(request,id):
     return render(request,'ADMIN/Classroom/Delete-Classroom.html')

#------------ViewEnrollment--------------#
# ViewEnrollment
def ViewEnrollment(request):
    return render(request,'ADMIN/Enrollment/View-Enrollment.html')
def UpdateEnrollment(request,id):
    if request.method=='POST':
        return redirect('ViewEnrollment')
    return render(request,'ADMIN/Enrollment/Update-Enrollment.html')
def AddEnrollment(request):
    return render(request,'ADMIN/Enrollment/Add-Enrollment.html')
def DeleteEnrollment(request,id):
    return render(request,'ADMIN/Enrollment/Delete-Enrollment.html')

# ----finance -------#
# ViewPayment
def ViewPayment(request):
    return render(request,'ADMIN/Payment/View-Payments.html')

        # AddPayment
def AddPayment(request):
    return render(request,'ADMIN/Payment/Add-Payment.html')
#   UpdatePayment
def UpdatePayment(request,id):
    return render(request,'ADMIN/Payment/Update-Payment.html')
# DeletePayment
def DeletePayment(request,id):
    return render(request,'ADMIN/Payment/Delete-Payment.html')
# dues and overdues 
def DuesAndOverDues(request):
    return render(request,'ADMIN/Payment/Dues_overdues/OverDue.html')

#-------Schedule 
# ViewSchedule
def ViewSchedule(request):
    return render(request,'ADMIN/Schedule/View-Schedule.html')

# DeleteSchedule
def DeleteSchedule(request,id):
    return render(request,'ADMIN/Schedule/Delete-Schedule.html')
# AddSchedule
def AddSchedule(request):
    return render(request,'ADMIN/Schedule/Add-Schedule.html')
# FreeRoom
def FreeRoom(request):
    return render(request,'ADMIN/Schedule/Free-Room.html')
# -----Downloads-----#
def Downloads(request):
    return render(request,'ADMIN/Exports/Export.html')

# -----Analytics---------#
# studentpercourse
def studentpercourse(request):
    return render(request,'ADMIN/Analytic/Student-Per-Course.html')

# first page for the viewer 
def ViewerDashboard(request):
    return render(request,'ADMIN/Viewer-Dashboard.html')
