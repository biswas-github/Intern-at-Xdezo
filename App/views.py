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

# -----Instructor-------
def Instructor(request):
    return render(request,'ADMIN/Instructor/Instructor.html')

# first page for the viewer 
def ViewerDashboard(request):
    return render(request,'ADMIN/Viewer-Dashboard.html')
