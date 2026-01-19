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





#------------ViewEnrollment--------------#
# ViewEnrollment
def ViewEnrollment(request):
    enrollments=[]
    try:
        enroll1 = get_list_or_404(Enrollment.objects.order_by('-id'))
        print(enroll1)
        data=[]
        for enroll in enroll1:
            data.append(
                {
                    "id":enroll.id,
                    "student_name":enroll.student.full_name,
                    "batch_name":enroll.batch.name,
                    "enrolled_date":enroll.enrolled_on,
                    "status":enroll.status,
                }
            )
            enrollments=data
        
    except Exception as e:
        messages.error(request, "Data Not found !")
    context = {
        'enrollments': enrollments
    }
    return render(request, 'ADMIN/Enrollment/View-Enrollment.html', context)


def UpdateEnrollment(request, id):
    # Fetch the object once (used for both GET to display and POST to update)
    enrollment = get_object_or_404(Enrollment, id=id)

    if request.method == 'POST':
        try:
            # 1. Get data from the form
            student_id = request.POST.get('student')
            batch_id = request.POST.get('batch')
            status_val = request.POST.get('status')
            enrolled_on_val = request.POST.get('enrolled_on') # Get the date string

            # 2. Update the fields
            enrollment.student_id = student_id 
            enrollment.batch_id = batch_id
            enrollment.status = status_val
            
            # Update the date (Ensure your HTML input name is 'enrolled_on')
            if enrolled_on_val: 
                enrollment.enrolled_on = enrolled_on_val

            # 3. Save
            enrollment.save()
            
            messages.success(request, "Enrollment updated successfully!")
            return redirect('ViewEnrollment')

        except IntegrityError:
            messages.error(request, "This student is already enrolled in this batch!")
        except Exception as e:
            messages.error(request, f"Error updating enrollment: {e}")

    # --- GET REQUEST ---
    # We only need to fetch the lists here. 'enrollment' is already fetched at the top.
    students = get_list_or_404(Student)
    batches = get_list_or_404(Batch)

    context = {
        "enrollment": enrollment,
        "students": students,
        "batches": batches
    }
    return render(request, 'ADMIN/Enrollment/Update-Enrollment.html', context)

def AddEnrollment(request):
    if request.method == "POST":
        try:
            # 1. Extract data
            student_id = request.POST.get('student')
            batch_id = request.POST.get('batch')
            status_val = request.POST.get('status')

            # 2. Create the Enrollment
            # We use student_id and batch_id to avoid fetching the full objects first
            enrollment = Enrollment(
                student_id=student_id,
                batch_id=batch_id,
                status=status_val
            )
            
            # 3. Save to DB
            enrollment.save()

            messages.success(request, "Student enrolled successfully!")
            return redirect('ViewEnrollment')

        except IntegrityError:
            # This handles the unique_together constraint (Double entry)
            messages.error(request, "This student is already enrolled in this batch!")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    # --- GET REQUEST ---
    # Fetch all students and batches to populate the dropdowns
    students = Student.objects.all()
    batches = Batch.objects.all()

    context = {
        'students': students,
        'batches': batches
    }
    return render(request, 'ADMIN/Enrollment/Add-Enrollment.html', context)

def DeleteEnrollment(request,id):
    try:
        en=get_object_or_404(Enrollment,id=id)
        name=en.student.full_name
        course=en.batch.course.title
        en.delete()
        messages.success(request,f"Enrollment deleted for student {name} on course{course}")
    except Exception as e:
        messages.success(request,f"Enrollment NOT deleted")

    return render(request,'ADMIN/Enrollment/Delete-Enrollment.html')

# ----finance -------#
# ViewPayment
def ViewPayment(request):
    # Fetch all payments using standard queryset without select_related
    payments_data = []
    try:
        payments_qs = Payments.objects.all().order_by('-date')
        # Create the list with mapped fields for the template

        for payment in payments_qs:
            if payment.enrollment:
                batch_info= payment.enrollment.batch.name
                student_info=payment.enrollment.student.full_name
            else:
                student_info=payment.student.full_name
                batch_info="General payment"
            payments_data.append({
                'id': payment.id,
                'student':  student_info,      
                'batch':batch_info,     
                'amount': payment.amount,
                'date': payment.date,
                'method': payment.method,
                'reference_no': payment.ref_no,  
                'remarks': payment.remarks,
            })
            
    except:
        if len(payments_data)<=0:
            print("no payments")
            messages.error(request,"No Data found for Payments")
            pass
        
    
    context = {
        'payments': payments_data
    }
    return render(request, 'ADMIN/Payment/View-Payments.html', context)

        # AddPayment
def AddPayment(request):
    if request.method == 'POST':
        # 1. Retrieve data from the HTML form
        student_id = request.POST.get('student')
        enrollment_id = request.POST.get('enrollment')  # Optional
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        ref_no = request.POST.get('ref_no')
        remarks = request.POST.get('remarks')
        
        if enrollment_id:
            enrollment_obj = get_object_or_404(Enrollment, id=enrollment_id)
            student_obj = enrollment_obj.student  # Auto-fill student from enrollment
        else:
            # If no enrollment, then Student ID is REQUIRED manually
            if not student_id:
                messages.error(request, "Please select a student OR the enrollment to the student")
                return redirect('add_payment')
            student_obj = get_object_or_404(Student, id=student_id)
            enrollment_obj = None
        
        try:
            # 3. Save to Database
            # We use atomic transaction to ensure data integrity
            from django.db import transaction
            with transaction.atomic():
                Payments.objects.create(
                    student=student_obj,
                    enrollment=enrollment_obj,
                    amount=amount,
                    method=method,
                    ref_no=ref_no,
                    remarks=remarks
                )
            print(f"student {student_id},enroll {enrollment_id} amt {amount} method {method}")
            messages.success(request, f"Payment of Rs. {amount} added successfully for {student_obj.full_name}.")
            return redirect('ViewPayment')

        except ValidationError as e:
            # Capture model validation errors
            messages.error(request, f"Error: {e}")
        except Exception as e:
            # Capture other database errors
            messages.error(request, f"An unexpected error occurred: {e}")
            
    # --- GET Request (Display the Form) ---
    
    students = Student.objects.all().order_by('-id')
    
    # Fetch active enrollments (optimized with select_related)
    # We display the Batch name in the dropdown so the user knows what they are paying for
    enrollments = Enrollment.objects.filter(status=Enrollment.Status.ACTIVE).select_related('batch', 'student').order_by('-enrolled_on')

    context = {
        'students': students,
        'enrollments': enrollments,
    }
    return render(request, 'ADMIN/Payment/Add-Payment.html', context)     

#   UpdatePayment
def UpdatePayment(request, id):
    payment = get_object_or_404(Payments, id=id)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        enrollment_id = request.POST.get('enrollment')
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        ref_no = request.POST.get('ref_no')
        remarks = request.POST.get('remarks')

        try:
            # --- FIX STARTS HERE ---
            
            # Logic: If Enrollment is chosen, get Student FROM Enrollment.
            # Otherwise, use the manually selected Student ID.
            
            if enrollment_id:
                # 1. Fetch Enrollment First
                enrol_obj = get_object_or_404(Enrollment, id=enrollment_id)
                payment.enrollment = enrol_obj
                
                # 2. Auto-set Student from that Enrollment
                # This fixes the issue where student_id is empty because JS hid the field
                student_obj = enrol_obj.student  
                payment.student = student_obj
                
            else:
                # Fallback: No enrollment, so we MUST have a student_id
                if not student_id:
                    messages.error(request, "Student is required for general payments.")
                    return redirect('UpdatePayment', id=id)
                    
                student_obj = get_object_or_404(Student, id=student_id)
                payment.student = student_obj
                payment.enrollment = None
            
            # --- FIX ENDS HERE ---

            payment.amount = amount
            payment.method = method
            payment.ref_no = ref_no
            payment.remarks = remarks
            
            payment.save()
                
            messages.success(request, f"Payment updated successfully for {student_obj.full_name}")
            return redirect('ViewPayment')

        except Exception as e:
            messages.error(request, f"Error updating payment: {e}")

    # GET Request logic remains the same
    students = Student.objects.filter(status=Student.Status.ACTIVE).order_by('full_name')
    enrollments = Enrollment.objects.filter(status=Enrollment.Status.ACTIVE).select_related('batch', 'student')

    context = {
        'payment': payment,
        'students': students,
        'enrollments': enrollments,
    }
    return render(request, 'ADMIN/Payment/Update-Payment.html', context)

# DeletePayment
def DeletePayment(request,id):
    if id:
        try:
            # Fetch and delete the payment
            pay = get_object_or_404(Payments, id=id)
            pay.delete()
            
            print(f"Delete success")
            messages.success(request,f"Deleted the payment successfully for <strong>{pay.student.full_name}</strong>")
            return render(request, 'ADMIN/Payment/Delete-Payment.html') 

        except Exception as e:
            print(f"Delete failed: {e}")
            messages.error(request, "Failed to delete payment.")

    return render(request, 'ADMIN/Payment/Delete-Payment.html')
# dues and overdues 
def DuesAndOverDues(request):
    due_list = [
        {
            'name': 'Bishal Gurung',
            'batch': 'Graphic Design',
            'course': 'Graphic Design',
            'total_fee': 12000,
            'paid_amount': 0,
            'due_amount': 12000,
            'status_code': 'overdue'
        }]
    # today = timezone.localdate()
    today=date.today()
    
    enrollments = Enrollment.objects.select_related("student", "batch", "batch__course")

    report = []
    for e in enrollments:
        course_fee = e.batch.course.Course_fee or 0
        batch_start_date = e.batch.start_date

        # Sum payments only for this enrollment (ignore "general payments")
        paid_all = (
            Payments.objects
            .filter(enrollment=e))  
        sum=0              # only enrollment payment
        for data in paid_all:
            sum+=data.amount
        paid=sum
        due = course_fee - paid
        status=""
        if due==0 or due<0:
            continue
        else:
            if batch_start_date>today:
                status="pending"
            if batch_start_date<=today:
                status="overdue"
            

        started = batch_start_date <= today

        due_list.append({
            "name": e.student.full_name if e.student else None,
            "course": e.batch.course.title if e.batch and e.batch.course else None,
            "batch": e.batch.name if e.batch else None,
            "batch_start_date": batch_start_date,
            "total_fee": course_fee,
            "paid_amount": paid,
            "due_amount": due,
            "status_code": status,
            "batch_started": started,
        })
    
    
    
    context = {
        'due_list': due_list
    }
    return render(request,'ADMIN/Payment/Dues_overdues/OverDue.html',context)

#-------Schedule 
# ViewSchedule
def ViewSchedule(request):
    import datetime
    today = datetime.date.today()
    schedules=[]
    instructors=[]
    try:
        schedules = get_list_or_404(
        Schedule.objects.select_related('batch', 'classroom', 'instructor').order_by('-date'))
        
    except:
        messages.error(request,"No data found !")

    # 2. Fetch instructors for the filter dropdown (optional, but needed for your UI)
    try:
        instructors = get_list_or_404(Instructor.objects.all())
    except:
        messages.error(request,"No instructor found !")

    context = {
        'schedules': schedules,
        'instructors': instructors
    }
    return render(request, 'ADMIN/Schedule/View-Schedule.html', context)


# DeleteSchedule
def DeleteSchedule(request,id):
    try:
        sched=get_object_or_404(Schedule,id=id)
        if sched:
            s_date=sched.date
            s_time=sched.start_time
            s_batch=sched.batch.name
            sched.delete()
            messages.success(request,f"Schedule Deleted fron the DB date :{s_date}  time: {s_time} batch: {s_batch}")
    except Exception as e:
        messages.error(request,"Data cant be deleted ")
        print(e)
    return render(request,'ADMIN/Schedule/Delete-Schedule.html')
# AddSchedule
def AddSchedule(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        try:
            # 1. Fetch the Batch immediately (We need it for both Recurring and Single)
            batch_id = request.POST.get('batch')
            batch = get_object_or_404(Batch, id=batch_id)

            # 2. Determine the Instructor
            # Logic: If form has instructor -> Use it.
            #        Else if Batch has instructor -> Use Batch's instructor.
            #        Else -> None.
            form_instructor_id = request.POST.get('instructor')
            
            final_instructor_id = None

            if form_instructor_id:
                # User manually selected an instructor (Overrides batch default)
                final_instructor_id = form_instructor_id
            elif hasattr(batch, 'instructor') and batch.instructor:
                # User left it blank, but Batch has a default instructor assigned
                final_instructor_id = batch.instructor.id

            # 3. Clean Classroom Data
            classroom_id = request.POST.get('classroom')
            if not classroom_id: 
                classroom_id = None

           
            if form_type == 'recurring':
                # Get days as integers (Match your HTML value="0" to Python's 0)
                selected_days = [int(d) for d in request.POST.getlist('days')]
                
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')

                if not batch.start_date or not batch.end_date:
                    raise ValueError("Batch does not have valid Start/End dates.")

                schedules_to_create = []
                current_date = batch.start_date

                while current_date <= batch.end_date:
                    # Check if current day (0=Mon...6=Sun) matches user selection
                    if current_date.weekday() in selected_days:
                        schedules_to_create.append(
                            Schedule(
                                batch=batch,
                                date=current_date,
                                start_time=start_time,
                                end_time=end_time,
                                # Uses Form or Batch default
                                instructor_id=final_instructor_id, 
                                classroom_id=classroom_id,
                                status='SCHEDULED'
                            )
                        )
                    current_date += timedelta(days=1)

                if schedules_to_create:
                    Schedule.objects.bulk_create(schedules_to_create)
                    messages.success(request, f"Generated {len(schedules_to_create)} sessions. (Instructor: {Instructor.objects.get(id=final_instructor_id).full_name or 'TBA'})")
                else:
                    messages.warning(request, "No dates matched within the batch duration.")
                
                return redirect('ViewSchedule')

         
            elif form_type == 'single':
                date_val = request.POST.get('date')
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                status_val = request.POST.get('status')

                Schedule.objects.create(
                    batch=batch,
                    date=date_val,
                    start_time=start_time,
                    end_time=end_time,
                    instructor_id=final_instructor_id, # Uses Form or Batch default
                    classroom_id=classroom_id,
                    status=status_val
                )
                
                messages.success(request, "Single session added successfully!")
                return redirect('ViewSchedule')

        except Exception as e:
            messages.error(request, f"Error: {e}")

    # --- GET REQUEST ---
    try:
        # Use get_list_or_404 for batches (as requested)
        batches = get_list_or_404(Batch)
        
        # Keep .all() for these so page doesn't crash if empty
        instructors = Instructor.objects.all()
        classrooms = Classroom.objects.all()
    except:
        batches = []
        instructors = []
        classrooms = []
        messages.warning(request, "No Batches found. Please create a Batch first.")

    context = {
        'batches': batches,
        'instructors': instructors,
        'classrooms': classrooms
    }
    return render(request, 'ADMIN/Schedule/Add-Schedule.html', context)


# EditSchedule
def EditSchedule(request,id):
    schedule = get_object_or_404(Schedule, id=id)

    if request.method == "POST":
        try:
            # 2. Extract Data
            batch_id = request.POST.get('batch')
            date_val = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            status_val = request.POST.get('status')
            
            # Special handling for Optional Fields (Instructor/Classroom)
            # If value is an empty string "", we must set it to None (Null)
            instructor_id = request.POST.get('instructor') or None
            classroom_id = request.POST.get('classroom') or None

            # 3. Update Object Fields
            schedule.batch_id = batch_id
            schedule.date = date_val
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.status = status_val
            schedule.instructor_id = instructor_id
            schedule.classroom_id = classroom_id

            # 4. Save Changes
            schedule.save()

            messages.success(request, "Schedule updated successfully!")
            return redirect('ViewSchedule')

        except Exception as e:
            messages.error(request, f"Error updating schedule: {e}")
            return redirect('ViewSchedule')

    # --- GET REQUEST ---
    # Fetch lists for the dropdowns
    batches = Batch.objects.all()
    instructors = Instructor.objects.all()
    classrooms = Classroom.objects.all()

    context = {
        'schedule': schedule,
        'batches': batches,
        'instructors': instructors,
        'classrooms': classrooms
    }
    return render(request, 'ADMIN/Schedule/Edit-Schedule.html', context)

# FreeRoom
def FreeRoom(request):
    free_rooms = []

    # Get data from URL
    user_date = request.GET.get('date')
    user_start = request.GET.get('start_time')
    user_end = request.GET.get('end_time')

    if user_date and user_start and user_end:
        try:
            # --- STEP 1: Find schedules that conflict ---
            # "Find schedules on this date where time overlaps"
            busy_schedules = Schedule.objects.filter(
                date=user_date,
                status='SCHEDULED',
                start_time__lt=user_end, # Starts before we finish
                end_time__gt=user_start  # Ends after we start
            )

            # --- STEP 2: Create a list of Busy Room IDs ---
            # We loop through the schedules and write down the Room ID in a list.
            busy_ids = []
            for schedule in busy_schedules:
                # Check if a classroom is assigned to avoid errors
                if schedule.classroom:
                    busy_ids.append(schedule.classroom.id)
            
            # Example result: busy_ids = [1, 5]


            # --- STEP 3: Check every room one by one ---
            # Get all active rooms
            all_rooms = Classroom.objects.filter(is_active=True)

            # Loop through every room in the school
            for room in all_rooms:
                # If the room's ID is NOT in our busy list, it is free!
                if room.id not in busy_ids:
                    free_rooms.append(room)

        except Exception as e:
            print(e)
            messages.error(request, "Error searching.")

    context = {
        'free_rooms': free_rooms
    }
    return render(request, 'ADMIN/Schedule/Free-Room.html', context)
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
