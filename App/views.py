from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
def LoginPage(request):
    if request.method=='GET':
        return render(request,'auth/login.html')
    if request.method=='POST':
        # if correct credential 
        role=request.POST.get('role') 
        if role=='ADMIN':
            return redirect('AdminDashboard')
        elif role=='VIEWER':
            return redirect(request,'ViewerDashboard')

# admin dashboard after login 
def AdminDashboard(request):
    return render(request,'ADMIN/Admin-Dashboard.html')


# first page for the viewer 
def ViewerDashboard(request):
    return render(request,'ADMIN/Viewer-Dashboard.html')
