from django.shortcuts import render,redirect, get_object_or_404,get_list_or_404
from django.http import HttpResponse,Http404
from datetime import date
# time delta is used for incrementting or decrement by some days 
# eg:  # Move to next day
# current_date += timedelta(days=1)
from datetime import timedelta
from django.contrib import messages
from .models import Course,Instructor,Batch,Classroom,Schedule,Payments
from django.db import IntegrityError
from django.core.exceptions import ValidationError

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
# Signup
def Signup(request):
    return render(request,'auth/Signup.html')
# ---------User management---------------#
#  ViewSystemUser
from datetime import datetime, timedelta


# admin dashboard after login 
def AdminDashboard(request):
    return render(request,'ADMIN/Admin-Dashboard.html')






# -----Downloads-----#
def Downloads(request):
    return render(request,'ADMIN/Exports/Export.html')



# first page for the viewer 
def ViewerDashboard(request):
    return render(request,'ADMIN/Viewer-Dashboard.html')


# DOwnload files 
def download_report(request):
    import os
    from django.conf import settings
    from django.http import FileResponse, Http404, HttpResponseForbidden
    from django.contrib.auth.decorators import login_required
    # Optional: restrict to staff/admin only
  

    file_path = os.path.join(settings.PRIVATE_ROOT, "data.csv")
    print("abc")
    if not os.path.exists(file_path):
        raise Http404("File not found.")

    # 'as_attachment=True' forces download
    # 'filename=' controls the downloaded name
    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="data.csv"
    )
