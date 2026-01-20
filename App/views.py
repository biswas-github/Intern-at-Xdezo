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
    revenue_labels = ["July", "August", "September", "October", "November", "December"]
    revenue_data = [45000, 52000, 48000, 61000, 75000, 92000]
    
    # Calculate total for the badge: "Total: Rs. 373,000"
    total_revenue_sum = sum(revenue_data)

    # --- 2. Dummy Enrollment Data (Bar Chart) ---
    # In a real app, you would query your Student model here.
    enrollment_labels = ["may","July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    enrollment_data = [15, 22, 18, 30, 25, 42,1]

    context = {
        # ... your existing KPIs (active_students, etc.) ...
        
        # Keys must match what is used in the {{ variable|json_script }} tags
        'chart_labels': revenue_labels,
        'chart_data': revenue_data,
        'total_revenue': "{:,}".format(total_revenue_sum), # Adds comma (e.g., 92,000)
        
        'enrollment_labels': enrollment_labels,
        'enrollment_data': enrollment_data,
    }

    return render(request,'ADMIN/Admin-Dashboard.html',context)






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
