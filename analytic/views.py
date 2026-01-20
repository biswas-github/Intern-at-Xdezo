from django.shortcuts import render

# Create your views here.


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
from App.models import Student, Enrollment

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
from App.models import Enrollment
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
