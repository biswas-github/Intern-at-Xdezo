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

# -----Analytics---------#
# studentpercourse
def studentpercourse(request):
#   from django.shortcuts import render
# from .models import Course, Enrollment
#    ---------------------------------------#
    # # 1. Fetch all courses
    # courses = Course.objects.all()
    
    # # 2. Prepare lists for Chart.js
    # course_titles = []
    # student_counts = []

    # for course in courses:
    #     # Logic: Count Enrollments where the Batch belongs to this Course
    #     # Course -> Batch -> Enrollment
    #     count = Enrollment.objects.filter(batch__course=course).count()
        
    #     course_titles.append(course.title)  # The X-Axis Labels
    #     student_counts.append(count)        # The Y-Axis Data

        
        # ------------------------------------------------#
    course_titles = ( ["python", "React", "js", "example"]) * 6
  # 4 × 25 = 100 items

    student_counts =  ([50, 10, 60, 100] )* 6
  # 4 × 25 = 100 items

    context = {
        # Pass these lists to the template
        'chart_labels': course_titles, 
        'chart_data': student_counts,
    }
    
    return render(request, 'ADMIN/Analytic/Student-Per-Course.html', context)
# MonthlyRevenue


def MonthlyRevenue(request):
    # ------------------------------------------#
    # from django.shortcuts import render
    # from .models import Payments
    # # 1. Get ALL payments from the database, sorted by date
    # all_payments = Payments.objects.all().order_by('date')

    # # 2. Create a "Dictionary" to hold our running totals
    # # It will look like this: { "January 2026": 50000, "February 2026": 20000 }
    # monthly_totals = {}

    # # 3. Loop through every single payment (The Simple Logic)
    # for payment in all_payments:
    #     # Convert the payment date to a string like "January 2026"
    #     month_name = payment.date.strftime('%B %Y')
        
    #     # Convert Decimal to Float for math
    #     amount = float(payment.amount)

    #     # Check: Have we seen this month before?
    #     if month_name in monthly_totals:
    #         # Yes: Add this amount to the existing total
    #         monthly_totals[month_name] += amount
    #     else:
    #         # No: Start a new total for this month
    #         monthly_totals[month_name] = amount

    # # 4. Prepare Data for the HTML Template
    # # Chart.js needs two separate lists: Labels (Months) and Data (Amounts)
    # chart_labels = list(monthly_totals.keys())   # ['Jan 2026', 'Feb 2026']
    # chart_data = list(monthly_totals.values())   # [50000, 20000]
    # ------------------------------------------#
    monthly_totals = {
        "January 2025": 45000.00,
        "February 2025": 32000.50,
        "March 2025": 58000.00,
        "April 2025": 12500.00,
        "May 2025": 67000.00,
        "June 2025": 41000.00
    }
    chart_labels = list(monthly_totals.keys())
    chart_data = list(monthly_totals.values())


    # 5. Prepare Data for the Table (List of Dictionaries)
    table_data = []
    for month, total in monthly_totals.items():
        table_data.append({
            'month': month,
            'amount': total,
            'count': 'N/A' # Keeping it simple (skipping transaction count)
        })

    # 6. Calculate Grand Total
    grand_total = sum(chart_data)

    context = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'table_data': table_data,
        'total_revenue': grand_total
    }

    return render(request, 'ADMIN/Analytic/monthly-Revenue.html', context)
# ActiveStudent
def ActiveStudent(request):
    from django.shortcuts import render
from .models import Student, Enrollment

def ActiveStudent(request):
    """
    Beginner-Friendly View.
    Logic: Fetch data -> Loop through it -> Count manually with Python.
    """

    # ================================================================= #
    #                 1. ACTUAL CODE (COMMENTED OUT)                    #
    # ================================================================= #
    """
    # --- PART A: CALCULATE CHART DATA (The Python Way) ---
    # 1. Fetch ALL students
    all_students = Student.objects.all()

    # 2. Initialize counters
    count_active = 0
    count_completed = 0
    count_dropped = 0
    count_inactive = 0

    # 3. Loop through every student and check their status
    for student in all_students:
        if student.status == 'ACTIVE':
            count_active += 1
        elif student.status == 'COMPLETED':
            count_completed += 1
        elif student.status == 'DROPPED':
            count_dropped += 1
        else:
            count_inactive += 1
    
    # 4. Prepare Lists for Chart.js
    chart_labels = ["Active", "Completed", "Inactive", "Dropped"]
    chart_data = [count_active, count_completed, count_inactive, count_dropped]


    # --- PART B: CALCULATE TABLE DATA (Recent Active Students) ---
    # 1. Get the 5 newest students who are ACTIVE
    recent_students = Student.objects.filter(status='ACTIVE').order_by('-created_at')[:5]
    
    table_data = []

    # 2. Loop through them to find extra details (like Batch)
    for std in recent_students:
        
        # Find which batch they are in (Get the first enrollment found)
        # We look in the 'Enrollment' table where student is 'std'
        enrollment = Enrollment.objects.filter(student=std).first()
        
        # Handle case if they haven't enrolled in a batch yet
        if enrollment:
            batch_name = enrollment.batch.name
        else:
            batch_name = "Not Assigned"

        # Add to list
        table_data.append({
            "name": std.full_name,
            "batch": batch_name,
            "joined": std.created_at.strftime('%b %d, %Y'), # Format date
            "progress": 0 # Dummy value (Calculating real progress is complex)
        })

    # --- PART C: KPIs ---
    total_active = count_active
    growth_rate = "+5%" # Hardcoded for now
    """

    # ================================================================= #
    #                       2. DUMMY DATA (FOR UI TESTING)              #
    # ================================================================= #
    
    # Chart Data
    chart_labels = ["Active", "Completed", "Inactive", "Dropped"]
    chart_data = [120, 45, 15, 5]  
    
    total_active = 120 
    growth_rate = "+12%" 

    # ================================================================= #

    context = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
      
        'total_active': total_active,
        'growth_rate': growth_rate
    }
    return render(request,'ADMIN\Analytic\Active-Students.html',context)
# Enrollments trends 
from django.shortcuts import render
from .models import Enrollment
from datetime import datetime
# analytics_enrollment_trends
def analytics_enrollment_trends(request):
    # -------------------------#
    # # 1. Fetch all enrollments sorted by date (Oldest first)
    # all_enrollments = Enrollment.objects.all().order_by('enrolled_on')

    # # 2. Create a dictionary to count enrollments per month
    # # Format: { "January 2025": 10, "February 2025": 15 }
    # monthly_counts = {}

    # for enroll in all_enrollments:
    #     # Convert date to string "Month Year" (e.g., "Jan 2026")
    #     month_label = enroll.enrolled_on.strftime('%b %Y')
        
    #     if month_label in monthly_counts:
    #         monthly_counts[month_label] += 1
    #     else:
    #         monthly_counts[month_label] = 1

    # # 3. Separate into Lists for Chart.js
    # chart_labels = list(monthly_counts.keys())  # X-Axis
    # chart_data = list(monthly_counts.values())  # Y-Axis

    # # 4. KPIs (Big Numbers)
    # total_enrollments = all_enrollments.count()
    
    # # Calculate Peak Month (Highest number of enrollments)
    # peak_count = 0
    # if chart_data:
    #     peak_count = max(chart_data)
    # -------------------------#
    


# dummy data 
     # X-Axis: The last 6 months
    chart_labels = ["Aug 2025", "Sep 2025", "Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026"]
    
    # Y-Axis: How many students joined in those months
    chart_data = [15, 22, 18, 35, 45, 60]  

    # KPIs
    total_enrollments = 250  # Total students in history
    peak_count = 60  

    context = {
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'total_enrollments': total_enrollments,
        'peak_count': peak_count
    }

    return render(request, 'ADMIN/Analytic/analytics_enrollment_trends.html', context)

# --------system logs -----------#
# AllActivities
def AllActivities(request):
    activity_data = [
        {
           
            "type": "delete",  # Options: create, update, delete, login
            "badge_class": "badge-danger",
            "action_text": "DELETE",
            "description": "Removed Student Record",
            "target": "Ram Bahadur Thapa",
            "user": "System Admin",
            "date": "Jan 15, 2026 at 10:45 AM",
      
        },
        {
          
            "type": "update",
            "badge_class": "badge-warning",
            "action_text": "UPDATED",
            "description": "Changed Payment Status for",
            "target": "Invoice #INV-202",
            "user": "Sarah (Accountant)",
            "date": "Jan 15, 2026 at 09:30 AM",
       
        },
        {
           
            "type": "create",
            "badge_class": "badge-success",
            "action_text": "CREATED",
            "description": "Registered new Batch",
            "target": "Python Jan 2026",
            "user": "System Admin",
            "date": "Jan 14, 2026 at 04:15 PM",
      
        },
        {
       
            "type": "login",
            "badge_class": "badge-info",
            "action_text": "LOGIN",
            "description": "Successful login detected",
            "target": "", # Login might not have a bold target
            "user": "Amit Sharma (Instructor)",
            "date": "Jan 14, 2026 at 08:00 AM",
         
        },
         {
           
            "type": "Login",  # Options: create, update, delete, login
            "badge_class": "badge-info",
            "action_text": "LOGIN",
            "description": "Removed Student Record",
            "target": "hari Bahadur Thapa",
            "user": "Biswas ",
            "date": "Jan 65, 2026 at 10:45 AM",
      
        }
        ]

    context = {
        # We pass this list to be converted to JSON in the template
    'activities': activity_data 
    } 
    return render(request,"System-Logs/All-Activities.html",context)
# Export-Details
def ExportDetails(request):
    exports_data = [
        {"user": "Sarah Accountant", "type": "Monthly Payments", "date": datetime(2025, 12, 27, 14, 15)},
        {"user": "System Admin", "type": "Student Records", "date": datetime(2025, 12, 27, 11, 30)},
        {"user": "Amit Instructor", "type": "Attendance Sheet", "date": datetime(2025, 12, 27, 0, 45)},
        {"user": "System Admin", "type": "System Logs", "date": datetime(2025, 12, 26, 17, 20)},
        {"user": "Sarah Accountant", "type": "Dues Report", "date": datetime(2025, 12, 26, 15, 10)},
        {"user": "Sita Karki", "type": "Graphic Design Batch", "date": datetime(2025, 12, 26, 13, 00)},
        {"user": "System Admin", "type": "Active Batches", "date": datetime(2025, 12, 26, 10, 5)},
        {"user": "Ram Bahadur", "type": "Course List", "date": datetime(2025, 12, 25, 16, 45)},
        {"user": "Sarah Accountant", "type": "Invoice #9921", "date": datetime(2025, 12, 25, 14, 20)},
        {"user": "Amit Instructor", "type": "Python Syllabus", "date": datetime(2025, 12, 25, 9, 15)},
        {"user": "System Admin", "type": "Enrollment History", "date": datetime(2025, 12, 24, 18, 30)},
        {"user": "Hari Krishna", "type": "Exam Results", "date": datetime(2025, 12, 24, 12, 10)},
        {"user": "Sarah Accountant", "type": "Expense Report", "date": datetime(2025, 12, 24, 10, 50)},
        {"user": "System Admin", "type": "User List", "date": datetime(2025, 12, 23, 15, 40)},
        {"user": "Sita Karki", "type": "Attendance Sheet", "date": datetime(2025, 12, 23, 11, 25)},
        {"user": "Anisha KC", "type": "Student Records", "date": datetime(2025, 12, 23, 0, 15)},
        {"user": "Sarah Accountant", "type": "Tax Documents", "date": datetime(2025, 12, 22, 16, 55)},
        {"user": "System Admin", "type": "Backup Config", "date": datetime(2025, 12, 22, 14, 10)},
        {"user": "Amit Instructor", "type": "Python Jan 2026", "date": datetime(2025, 12, 22, 10, 5)},
        {"user": "Ram Bahadur", "type": "Fee Structure", "date": datetime(2025, 12, 21, 13, 30)},
        {"user": "Sarah Accountant", "type": "Pending Dues", "date": datetime(2025, 12, 21, 11, 45)},
        {"user": "System Admin", "type": "Audit Trail", "date": datetime(2025, 12, 20, 17, 20)},
        {"user": "Sita Karki", "type": "Assignment Grades", "date": datetime(2025, 12, 20, 15, 10)},
        {"user": "Hari Krishna", "type": "Course Materials", "date": datetime(2025, 12, 20, 12, 00)},
        {"user": "Sarah Accountant", "type": "Monthly Payments", "date": datetime(2025, 12, 19, 14, 50)},
        {"user": "System Admin", "type": "Student Records", "date": datetime(2025, 12, 19, 10, 30)},
        {"user": "Amit Instructor", "type": "Attendance Sheet", "date": datetime(2025, 12, 19, 9, 15)},
        {"user": "Anisha KC", "type": "Enrollment List", "date": datetime(2025, 12, 18, 16, 40)},
        {"user": "System Admin", "type": "Active Users", "date": datetime(2025, 12, 18, 13, 25)},
        {"user": "Sarah Accountant", "type": "Revenue Chart", "date": datetime(2025, 12, 18, 11, 10)},
        {"user": "Sita Karki", "type": "Class Schedule", "date": datetime(2025, 12, 17, 15, 55)},
        {"user": "Ram Bahadur", "type": "Certificates", "date": datetime(2025, 12, 17, 12, 40)},
        {"user": "System Admin", "type": "Database Dump", "date": datetime(2025, 12, 17, 0, 30)},
        {"user": "Sarah Accountant", "type": "Refund Requests", "date": datetime(2025, 12, 16, 16, 15)},
        {"user": "Amit Instructor", "type": "Project Submissions", "date": datetime(2025, 12, 16, 14, 20)},
        {"user": "Hari Krishna", "type": "Library Records", "date": datetime(2025, 12, 16, 10, 5)},
        {"user": "System Admin", "type": "Access Logs", "date": datetime(2025, 12, 15, 17, 00)},
        {"user": "Sarah Accountant", "type": "Salary Sheet", "date": datetime(2025, 12, 15, 11, 45)},
        {"user": "Sita Karki", "type": "Design Assets", "date": datetime(2025, 12, 15, 9, 30)},
        {"user": "System Admin", "type": "Full Backup", "date": datetime(2025, 12, 14, 23, 59)},
    ]

    context = {
        "exports": exports_data
    }
    
    return render(request, "System-Logs/Export-Details.html", context)
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
