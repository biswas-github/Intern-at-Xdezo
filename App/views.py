from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import date

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
def ViewSystemUser(request):
      # In a real model, you don't need this helper, the template calls user.get_full_name
    from datetime import datetime, timedelta
    users_list = [
        {
            "id": 1,
            "username": "admin_master",
            "email": "admin@college.edu",
            "first_name": "System",
            "last_name": "Admin",
            "get_full_name": "System Admin",
            "role": "ADMIN",          # Options: ADMIN, INSTRUCTOR, ACCOUNTANT, VIEWER
            "is_active": True,
            "date_joined": datetime(2024, 1, 1),
            "last_login": datetime.now() - timedelta(minutes=5)
        },
        {
            "id": 2,
            "username": "amit_py",
            "email": "amit.sharma@college.edu",
            "first_name": "Amit",
            "last_name": "Sharma",
            "get_full_name": "Amit Sharma",
            "role": "INSTRUCTOR",
            "is_active": True,
            "date_joined": datetime(2024, 2, 15),
            "last_login": datetime.now() - timedelta(hours=2)
        },
        {
            "id": 3,
            "username": "sarah_acct",
            "email": "sarah.accounts@college.edu",
            "first_name": "Sarah",
            "last_name": "Koirala",
            "get_full_name": "Sarah Koirala",
            "role": "ACCOUNTANT",
            "is_active": True,
            "date_joined": datetime(2024, 3, 10),
            "last_login": datetime.now() - timedelta(days=1)
        },
        {
            "id": 4,
            "username": "john_viewer",
            "email": "john.staff@college.edu",
            "first_name": "John",
            "last_name": "Doe",
            "get_full_name": "John Doe",
            "role": "VIEWER",
            "is_active": False,       # Simulating an inactive user
            "date_joined": datetime(2024, 5, 20),
            "last_login": datetime(2024, 12, 1)
        },
        {
            "id": 5,
            "username": "sita_graphic",
            "email": "sita.karki@college.edu",
            "first_name": "Sita",
            "last_name": "Karki",
            "get_full_name": "Sita Karki",
            "role": "INSTRUCTOR",
            "is_active": True,
            "date_joined": datetime(2024, 6, 1),
            "last_login": datetime.now() - timedelta(minutes=30)
        }
    ]

    context = {
        'users': users_list
    }

    return render(request,'ADMIN/UserManagement/View-System-User.html',context)
# AddSystemUser
def AddSystemUser(request):
    return render(request,'ADMIN/UserManagement/Add-System-User.html')
# EditUser
def EditUser(request,id):
    return render(request,'ADMIN/UserManagement/Edit-System-User.html')
# DeleteUser
def DeleteUser(request,id):
    return render(request,'ADMIN/UserManagement/Delete-System-User.html')

# admin dashboard after login 
def AdminDashboard(request):
    return render(request,'ADMIN/Admin-Dashboard.html')
# ----Students------#
# DataManagement-Student for managing the students 
def DataManagementStudent(request):
    return render(request,'ADMIN/DataManagement_Student.html')
# to view all the students
def ViewStudent(request):
    students = [
        {
            'id': 1,
            'name': 'Ram Bahadur Thapa',
            'phone': '9845123456',
            'email': 'ram.thapa@example.com',
            'dob': date(1998, 1, 1),
            'address': 'Kathmandu, Nepal',
            'status': 'Active'
        },
        {
            'id': 5,
            'name': 'Sita Kumari Shrestha',
            'phone': '9801122334',
            'email': 'sita.shrestha@example.com',
            'dob': date(1999, 2, 14),
            'address': 'Lalitpur, Nepal',
            'status': 'Inactive'
        },
        {
            'id': 2,
            'name': 'Bishal Gurung',
            'phone': '9865012345',
            'email': 'bishal.gurung@example.com',
            'dob': date(1999, 5, 15),
            'address': 'Pokhara, Nepal',
            'status': 'Dropped'
        },
        {
            'id': 6,
            'name': 'Anisha KC',
            'phone': '9812345678',
            'email': 'anisha.kc@example.com',
            'dob': date(2000, 3, 10),
            'address': 'Bhaktapur, Nepal',
            'status': 'Completed'
        }
    ]

    context = {
        'students': students
    }
    return render(request,'ADMIN/View-Student.html',context)
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
    courses = [
        {
            'id': 1,
            'title': 'Python with Django',
            'code': 'PY-101',
            'fee': '15,000',
            'duration': '3 Months',
            'description': 'The course focuses on full-stack development using the Django framework.'
        },
        {
            'id': 2,
            'title': 'Graphic Design',
            'code': 'GD-205',
            'fee': '12,000',
            'duration': '2 Months',
            'description': 'Learn fundamentals of visual communication, Photoshop and Illustrator.'
        },
        {
            'id': 3,
            'title': 'Digital Marketing',
            'code': 'DM-300',
            'fee': '10,000',
            'duration': '6 Weeks',
            'description': 'Master SEO, Social Media Marketing, and Content Strategy.'
        },
        {
            'id': 4,
            'title': 'Full Stack Web Development',
            'code': 'WD-401',
            'fee': '20,000',
            'duration': '4 Months',
            'description': 'Comprehensive training in HTML, CSS, JavaScript, React, Node.js, and MongoDB.'
        },
        {
            'id': 5,
            'title': 'Data Science with Python',
            'code': 'DS-500',
            'fee': '25,000',
            'duration': '5 Months',
            'description': 'Learn data analysis, visualization, machine learning algorithms, and Pandas/NumPy.'
        }
    ]

    context = {
        'courses': courses
    }
    return render(request,'ADMIN/View-Courses.html',context)
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
    batches = [
        {
            'id': 1,
            'name': 'Python Jan 2026 Morning',
            'course': 'Python Development (PY101)',
            'instructor': 'Mr. A. Sharma',
            'status': 'Upcoming',
            'start_date': date(2026, 1, 1),
            'end_date': date(2026, 3, 30)
        },
        {
            'id': 2,
            'name': 'Django Jan 2025 Morning',
            'course': 'Django Development (PY101)',
            'instructor': 'Ms. S. Karki',
            'status': 'Completed',
            'start_date': date(2024, 11, 22),
            'end_date': date(2025, 2, 25)
        },
        {
            'id': 3,
            'name': 'Graphic Design Evening',
            'course': 'Graphic Design Masterclass',
            'instructor': 'Mr. B. Rai',
            'status': 'Ongoing',
            'start_date': date(2025, 12, 1),
            'end_date': date(2026, 1, 30)
        }
    ]

    context = {
        'batches': batches
    }
    return render(request,'ADMIN/Batch/View-Batches.html',context)
# DeleteBatch
def DeleteBatch(request, id):
    return render(request,'ADMIN/BATCH/Delete-Batch.html')
# UpdateBatch
def UpdateBatch(request,id):
    return render(request,'ADMIN/BATCH/Update-Batch.html')

# -----Instructor-------
def Instructor(request):
    class MockUser:
            def __init__(self, username, first_name, last_name, email):
                self.username = username
                self.first_name = first_name
                self.last_name = last_name
                self.email = email
            
            def get_full_name(self):
                return f"{self.first_name} {self.last_name}"

    # 2. Mock the 'Instructor' Model
    # matching: user (OneToOne), phone, specialization, bio, is_active
    instructors = [
        {
            'id': 1,
            'user': MockUser('asharma', 'Amit', 'Sharma', 'amit.sharma@example.com'),
            'phone': '9841234567',
            'specialization': 'Python, Django, Backend',
            'bio': 'Senior backend developer with 5+ years of experience in Python ecosystems.',
            'is_active': True
        },
        {
            'id': 2,
            'user': MockUser('skarki', 'Sarita', 'Karki', 's.karki@example.com'),
            'phone': '9801987654',
            'specialization': 'Graphic Design (Ps, Ai)',
            'bio': 'Creative director passionate about UI/UX and visual storytelling.',
            'is_active': True
        },
        {
            'id': 3,
            'user': MockUser('brana', 'Bibek', 'Rana', 'b.rana@example.com'),
            'phone': '9860112233',
            'specialization': 'Digital Marketing, SEO',
            'bio': 'Certified digital marketer specializing in social media growth.',
            'is_active': False # Simulating an inactive instructor
        }
    ]

    context = {
        'instructors': instructors
        }

    return render(request,'ADMIN/Instructor/View-Instructor.html',context)
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
    classrooms=[
         {
            'id': 1,
            'name': 'Room 101',
            'capacity': 30,
            'is_active': True
        },
        {
            'id': 2,
            'name': 'Lab A - Computer Lab',
            'capacity': 25,
            'is_active': False
        },
        {
            'id': 3,
            'name': 'Conference Hall',
            'capacity': 100,
            'is_active': True
        },
         {
            'id': 2,
            'name': 'Lab A - Computer Lab',
            'capacity': 25,
            'is_active': False
        },
        {
            'id': 3,
            'name': 'Conference Hall',
            'capacity': 100,
            'is_active': True
        },
    ]
    context={
        "classrooms":classrooms}
    return render(request,'ADMIN/Classroom/View-Classroom.html',context)
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
    enrollments = [
        {
            'id': 1,
            'student_name': 'Ram Bahadur Thapa',
            'batch_name': 'Python Jan 2026',
            'enrolled_date': 'Jan 15, 2026',
            'status': 'Active'
        },
        {
            'id': 2,
            'student_name': 'Sita Kumari',
            'batch_name': 'Django Dec 2025',
            'enrolled_date': 'Dec 01, 2025',
            'status': 'Completed'
        },
        {
            'id': 3,
            'student_name': 'Hari Krishna',
            'batch_name': 'Graphic Design',
            'enrolled_date': 'Nov 10, 2025',
            'status': 'Dropped'
        }
    ]

    context = {
        'enrollments': enrollments
    }
    return render(request,'ADMIN/Enrollment/View-Enrollment.html',context)
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
    payments_data = [
        {
            'id': 1,
            'student': 'Ram Bahadur Thapa',
            'batch': 'Python Jan 2026',
            'amount': '15,000.00',
            'date': 'Jan 15, 2026',
            'method': 'ESEWA',
            'reference_no': 'ESW-987654321',
            'remarks': 'Full payment for Python course.'
        },
        {
            'id': 2,
            'student': 'Sita Kumari',
            'batch': 'Django Dec 2025',
            'amount': '5,000.00',
            'date': 'Dec 20, 2025',
            'method': 'BANK',
            'reference_no': 'TXN-882910',
            'remarks': 'First Installment via Nabil Bank.'
        },
        {
            'id': 3,
            'student': 'Hari Krishna',
            'batch': 'Graphic Design',
            'amount': '12,000.00',
            'date': 'Nov 10, 2025',
            'method': 'CASH',
            'reference_no': None, # Testing empty reference
            'remarks': 'Paid cash at the front desk.'
        },
        {
            'id': 4,
            'student': 'Kabita Joshi',
            'batch': 'UI/UX Design',
            'amount': '15,000.00',
            'date': 'Mar 05, 2026',
            'method': 'OTHERS',
            'reference_no': 'Phonpay-5566',
            'remarks': 'Paid via PhonePay QR.'
        },
        {
            'id': 5,
            'student': 'Anjali Sherpa',
            'batch': 'Web Dev 2026',
            'amount': '20,000.00',
            'date': 'Feb 01, 2026',
            'method': 'ESEWA',
            'reference_no': 'ESW-112233',
            'remarks': 'Full Payment including registration.'
        },
        {
            'id': 6,
            'student': 'Bibek Rana',
            'batch': 'Python Jan 2026',
            'amount': '7,500.00',
            'date': 'Jan 16, 2026',
            'method': 'BANK',
            'reference_no': 'CHQ-998877',
            'remarks': 'Cheque Payment - Part 1.'
        },
    ]

    context = {
        'payments': payments_data
    }
    return render(request,'ADMIN/Payment/View-Payments.html',context)

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
    due_list = [
        {
            'name': 'Ram Bahadur Thapa',
            'batch': 'Python Jan 2026',
            'course': 'Python Development',
            'total_fee': 15000,
            'paid_amount': 15000,
            'due_amount': 0,
            'status_code': 'cleared'
        },
        {
            'name': 'Sita Kumari',
            'batch': 'Django Dec 2025',
            'course': 'Django Framework',
            'total_fee': 15000,
            'paid_amount': 10000,
            'due_amount': 5000,
            'status_code': 'pending'
        },
        {
            'name': 'Bishal Gurung',
            'batch': 'Graphic Design',
            'course': 'Graphic Design',
            'total_fee': 12000,
            'paid_amount': 0,
            'due_amount': 12000,
            'status_code': 'overdue'
        }
    ]
    
    context = {
        'due_list': due_list
    }
    return render(request,'ADMIN/Payment/Dues_overdues/OverDue.html',context)

#-------Schedule 
# ViewSchedule
def ViewSchedule(request):
    import datetime
    today = datetime.date.today()
    
    schedules = [
        {
            'id': 1,
            'date': today,
            'start_time': '07:00',
            'end_time': '09:00',
            'batch': 'Python Jan 2026',
            'course': 'Python with Django',
            'classroom': 'Room 101',
            'instructor': 'Mr. A. Sharma',
            'status': 'SCHEDULED'
        },
        {
            'id': 2,
            'date': today + datetime.timedelta(days=2),
            'start_time': '10:00',
            'end_time': '12:00',
            'batch': 'Graphic Design A',
            'course': 'Graphic Design Masterclass',
            'classroom': 'Lab A',
            'instructor': 'Ms. S. Karki',
            'status': 'SCHEDULED'
        },
        {
            'id': 3,
            'date': today - datetime.timedelta(days=5),
            'start_time': '14:00',
            'end_time': '16:00',
            'batch': 'Web Dev 2025',
            'course': 'Full Stack Web',
            'classroom': 'Room 102',
            'instructor': 'Mr. B. Rai',
            'status': 'COMPLETED'
        },
         {
            'id': 4,
            'date': today + datetime.timedelta(days=1),
            'start_time': '08:00',
            'end_time': '10:00',
            'batch': 'Cyber Security',
            'course': 'Ethical Hacking',
            'classroom': 'Lab B',
            'instructor': 'Mr. C. Lama',
            'status': 'CANCELLED'
        }
    ]

    # Unique list of instructors for the filter dropdown
    instructors = list(set([s['instructor'] for s in schedules]))

    context = {
        'schedules': schedules,
        'instructors': instructors
    }
    return render(request,'ADMIN/Schedule/View-Schedule.html',context)

# DeleteSchedule
def DeleteSchedule(request,id):
    return render(request,'ADMIN/Schedule/Delete-Schedule.html')
# AddSchedule
def AddSchedule(request):
    return render(request,'ADMIN/Schedule/Add-Schedule.html')
# EditSchedule
def EditSchedule(request,id):
    return render(request,'ADMIN/Schedule/Edit-Schedule.html')

# FreeRoom
def FreeRoom(request):
    return render(request,'ADMIN/Schedule/Free-Room.html')
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
