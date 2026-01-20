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
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth

# Import your specific models
from .models import Student, Batch, Schedule, Payments, Classroom, Enrollment, Course

def AdminDashboard(request):
    # Get current date (needed to filter upcoming classes)
    today = timezone.now().date()

    # =======================================================
    # PART 1: KPI CARDS (The Big Numbers)
    # =======================================================

    # 1. Active Students
    # We filter by the status='ACTIVE' defined in your Student model
    active_students = Student.objects.filter(status=Student.Status.ACTIVE).count()

    # 2. Ongoing Batches
    ongoing_batches = Batch.objects.filter(status=Batch.Status.ONGOING).count()

    # 3. Today's Sessions
    # Count schedules where date matches today
    today_sessions = Schedule.objects.filter(date=today).count()

  # 4. Pending Dues Calculation
    
    # Step A: Total Collected (Same as before)
    # We sum all money received in the Payments table
    total_collected_data = Payments.objects.aggregate(total=Sum('amount'))
    total_collected = total_collected_data['total'] or 0 

    # Step B: Total Expected Fees (IMPROVED)
    # We sum fees ONLY for Active or Completed enrollments.
    # We EXCLUDE 'DROPPED' students so they don't mess up the calculation.
    total_expected_data = Enrollment.objects.exclude(
        status=Enrollment.Status.DROPPED
    ).aggregate(
        total=Sum('batch__course__Course_fee')
    )
    total_expected = total_expected_data['total'] or 0

    # Step C: The difference
    pending_dues = total_expected - total_collected
    
    # Optional: Handle negative dues (e.g., if you have data errors or overpayments)
    if pending_dues < 0:
        pending_dues = abs(pending_dues)
        pending_dues=round(pending_dues,2)
    
   
    # =======================================================
    # PART 2: DATA FOR CHARTS
    # =======================================================

    # --- CHART 1: MONTHLY REVENUE ---
    # Group 'Payments' by Month and Sum the 'amount'
    revenue_queryset = (
        Payments.objects
        .annotate(month=TruncMonth('date'))  # Group by Month
        .values('month')
        .annotate(total=Sum('amount'))       # Sum amount per month
        .order_by('month')
    )

    revenue_labels = []
    revenue_data = []

    for entry in revenue_queryset:
        # Convert date to string like "Jan", "Feb"
        revenue_labels.append(entry['month'].strftime('%b'))
        revenue_data.append(float(entry['total'])) # Ensure it's a number

    # --- CHART 2: ENROLLMENT TRENDS ---
    # Group 'Enrollment' by Month and Count IDs
    enrollment_queryset = (
        Enrollment.objects
        .annotate(month=TruncMonth('enrolled_on')) # Use enrolled_on field
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    enrollment_labels = []
    enrollment_data = []

    for entry in enrollment_queryset:
        enrollment_labels.append(entry['month'].strftime('%b'))
        enrollment_data.append(entry['count'])


    # =======================================================
    # PART 3: DATA TABLES
    # =======================================================

    # 1. Upcoming Schedules
    # Filter: Date is today or future. Order by Date then Start Time.
    upcoming_schedules = Schedule.objects.filter(
        date__gte=today,
        status=Schedule.Status.SCHEDULED
    ).order_by('date', 'start_time')[:5]

    # 2. Recent Payments
    # Order by date descending (newest first).
    # 'select_related' speeds up database queries by fetching student info at once.
    recent_payments = Payments.objects.select_related('student').order_by('-date')[:5]
    
    # 3. Available Rooms
    # Just listing all active rooms and their capacity
    rooms = Classroom.objects.filter(is_active=True)

    # =======================================================
    # PART 4: SEND TO TEMPLATE
    # =======================================================
    context = {
        # KPIs
        'active_students': active_students,
        'ongoing_batches': ongoing_batches,
        'today_sessions': today_sessions,
        'pending_dues': pending_dues, # e.g. "12,000"

        # Chart Data
        'chart_labels': revenue_labels,
        'chart_data': revenue_data,
        'total_revenue': "{:,}".format(total_collected),
        
        'enrollment_labels': enrollment_labels,
        'enrollment_data': enrollment_data,

        # Tables
        'upcoming_schedules': upcoming_schedules,
        'recent_payments': recent_payments,
        'rooms': rooms,
    }

    return render(request, 'ADMIN/Admin-Dashboard.html', context)




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
