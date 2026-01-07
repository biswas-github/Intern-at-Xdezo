from django.shortcuts import render,redirect, get_object_or_404,get_list_or_404
from django.http import HttpResponse,Http404
from datetime import date
from django.contrib import messages
from .models import Course,Instructor,Batch


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
    if request.method=="GET":
        return render(request,'ADMIN/UserManagement/Add-System-User.html')
    # if request.method=="POST":
    #     # register system user 
    #     role=request.POST['role']
    #     print(role)
    #     return render(request,'ADMIN/UserManagement/Add-System-User.html')
    

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
# add the student
def DataManagementStudent(request):
    if request.method=='GET':
        return render(request,'ADMIN/DataManagement_Student.html')
    if request.method=='POST':
        print("post method has hit")
        from .models import Student
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        Address=request.POST.get('Address')
        status=request.POST.get('status')
        print(name,email,phone,Address,status)
        try:
            if not phone.isdigit():
                messages.error(request,"phone number must include numbers only")
                return redirect('DataManagementStudent')

            if len(phone) != 10:
                messages.error(request,"phone number should be exact 10 digits")
                return redirect('DataManagementStudent')

            # register to the model
            Student.objects.create(full_name=name,email=email,phone=phone,address=Address,status=status)
            messages.success(request, "Student Added Sucessfully !")
            return redirect('ViewStudent')
        except Exception as e :
            # Other exceptions
            print(f"cant be done{e}")
            messages.error(request, "Student cant be added !")


      

        

        




    
# to view all the students
def ViewStudent(request):
    student = Student.objects.order_by('-id')
    if not student:
        # handle "not found" case
        raise Http404("No students found")  # optional


    students=[]
    for data in list(student):
        students.append(
            {
                 'id': data.id,
                 'name': data.full_name,
                 'phone': data.phone,
                 'email': data.email,
                 'address': data.address,
                 'status': data.status,
            }
        )

    context = {
        'students': students
    }
    return render(request,'ADMIN/View-Student.html',context)


# updating the student
def UpdateStudent(request,id):
    if request.method=="GET":
        data =get_object_or_404(Student, id=id)

        context= {
                        'id': data.id,
                        'name': data.full_name,
                        'phone': data.phone,
                        'email': data.email,
                        'address': data.address,
                        'status': data.status,
                    }
        return render(request,'ADMIN/Update-Student.html',context)
    if request.method=="POST":
        # extract data form the form
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        Address=request.POST.get('Address')
        status=request.POST.get('status')
        print(status)
        if len(phone)!=10:
            messages.warning(request,"phone number has to be at least 10 digits")
            return redirect(UpdateStudent,id)
        # student modal 
        try:
            student =get_object_or_404(Student, id=id)
            student.full_name=name
            student.email=email
            student.address=Address
            student.status=status
            student.phone=phone
            # save to the db
            student.save()
            # updated to the students 
            print("saved")
            messages.success(request, "Student  Updated")
            return redirect(ViewStudent)
            
        except Exception as e:
            print(f"the error is {e}")
            messages.error(request, "Student cant be Updated")
            return redirect(ViewStudent)


        
# delete the students
def DeleteStudent(request,id):
   
    student =get_object_or_404(Student, id=id)

    try:
        student.delete()
        # deleted
    except Exception as e:
        print("not deleted error {e}")
       
    return render(request,'ADMIN/Delete-Student.html')

# ----Courses------#
# DataManagement->courses for managing the Courses
def CourseRegister(request):
    if request.method=="GET":
        return render(request,'ADMIN/Courses.html')
    if request.method=="POST":
        # extract data
        title=request.POST.get('title')
        code=request.POST.get('code')
        fee=int(request.POST.get('fee'))
        Description=request.POST.get('Description')
        Duration=request.POST.get('Duration')
        print(f'all data that are recived are {title,code,fee,Description,Duration}')
        try:
            Course.objects.create(title=title,code=code,Course_fee=fee,description=Description,default_duration_weeks=int(Duration))
            print("course saves")
            messages.success(request,"cource added sucessfully")
        except:
            print("course not saved")
            messages.error(request,"cource added sucessfully")
        return redirect(ViewCourses)
       
    
def ViewCourses(request):
    if request.method=="GET":
        from .models import Course
        courses=[]
        try:
            all_course= get_list_or_404(Course)
            all_course.reverse()
            for data in all_course:
                courses.append(
                    {
                        "id":data.id,
                        "title":data.title,
                        "code":data.code,
                        "description":data.description,
                        "fee":data.Course_fee,
                        "duration":data.default_duration_weeks
                    }
                )
        
            context = {
            "courses": courses
        }
        except:
            courses=[]
            context = {
            "courses": courses
            }
            messages.error(request,"no courses found !")

        return render(request,'ADMIN/View-Courses.html',context)

  


def UpdateCourse(request,id):
    if request.method=="GET":
        try:
        # extract course 
            data=get_object_or_404(Course,id=id)
            course_data={
                "id":data.id,
                "title":data.title,
                "code":data.code,
                "description":data.description,
                "duration":data.default_duration_weeks,
                "fee":data.Course_fee
            }
            print(course_data)
            context={
                "course":course_data
            }
            return render(request,'ADMIN/Update-Course.html',context)
        except Exception as e:
            print(e)
            messages.warning(request,"Course not found")
            return redirect('ViewCourses')
            


    if request.method=="POST":
        # DO SOME LOGICS
        title=request.POST.get('title')
        print(title)
        code=request.POST.get('course_code')
        print(code)
        # from decimal import Decimal
        from decimal import Decimal
        fee = Decimal(request.POST.get('Fee'))
        print(fee)
        Description=request.POST.get('description')
        print(Description)
        Duration=request.POST.get('duration')
        print(Duration)
        try:
        # extract course 
            course=get_object_or_404(Course,id=id)
            # edit course
            if  course.title:
                course.title=title
            if  course.code:
                course.code=code
            if  course.Course_fee >0:
                course.Course_fee=fee
            else:
                messages.error(request,"Course fee should be a digit and greater than 0")
                return redirect(UpdateCourse)
            
            course.description=Description
            if not Duration.isdigit():
                messages.error(
                    request,
                    "Please enter duration in weeks using digits only (e.g. 2, 5, 12)"
                )
                return redirect(request.path)

            course.default_duration_weeks = int(Duration)
            # Save course 
            course.save()
            # send the message in the browser
            messages.success(request,"Course is Updated ")
            return redirect('ViewCourses')

        except Exception as e:
            print(e)
            messages.error(request,"Course is NOT Updated ")
            return redirect('ViewCourses')

    


def DeleteCourse(request,id):
    # find the course with the id
    course=get_object_or_404(Course,id=id)
    course_name=course.title
    try:
        course.delete()
        messages.success(request,f"the course  <strong>{course_name} </strong> is deleted successfully  ")
    except Exception as e:
        print(e)
        messages.error(request,"Course not deleted ")
        return redirect('ViewCourses')
    return render(request,'ADMIN/Delete-Course.html')
def ShowCourse(request,id):
    return render(request,'ADMIN/Show-Course.html')


# ----Batch------#
def AddBatch(request):
    # in the batch we need to send the all courses to the batch register
    if request.method=='GET':
        # courses
        try:
            courses=get_list_or_404(Course)
        except:
            messages.error(request,"First register to the course !")
            return redirect('ViewBatches')
        data=[]
        for course11 in courses:
            data.append(
                {
                    "id":course11.id,
                    "name":course11.title
                }
            )
        # instructors
        try:
            ins=get_list_or_404(Instructor)
        except:
            ins=None
        all_ins=[]
        if ins:
            all_ins=[]
            for instructor in ins:
                all_ins.append(
                    {
                        "id":instructor.id,
                        "name":instructor.user.username
                    }
                )
        context={
            "courses":data,
            "instructors":all_ins

        }
        return render(request,'ADMIN/Batch/Batch.html',context)
    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course')
        instructor_id = request.POST.get('instructor')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')

        # ---------- VALIDATIONS ----------
        if not name:
            messages.error(request, "Batch name is required")
            return redirect('Batch')

        if not course_id:
            messages.error(request, "Please select a course")
            return redirect('Batch')

        if not start_date or not end_date:
            messages.error(request, "Start date and end date are required")
            return redirect('Batch')

        # Convert dates
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('Batch')

        if start_date > end_date:
            messages.error(request, "Start date cannot be after end date")
            return redirect('Batch')
        try:
            
            course=get_object_or_404(Course,id=course_id)
        except Course.DoesNotExist:
            messages.error(request, "Selected course does not exist")
            return redirect('Batch')

        instructor = None
        if instructor_id:
            try:
                instructor=get_object_or_404(Instructor,id=instructor_id)
            except Instructor.DoesNotExist:
                messages.error(request, "Selected instructor does not exist")
                return redirect('Batch')

        # ---------- SAVE ----------
        Batch.objects.create(
            name=name,
            course=course,
            instructor=instructor,
            start_date=start_date,
            end_date=end_date,
            status=status or Batch.Status.UPCOMING,
        )

        messages.success(request, "Batch created successfully ")
        return redirect('ViewBatches')



 #viewbatches
def ViewBatches(request):
    try:
        batches = Batch.objects.select_related(
        'course',
        'instructor',
        'instructor__user'
        ).order_by('-id') or None
    except:
        messages.error(request,"something Error occured")
        return redirect("ViewBatches")
    
    return render(request, 'ADMIN/BATCH/View-Batches.html', {'batches': batches})

# DeleteBatch
def DeleteBatch(request, id):
    try:
        batch = get_object_or_404(Batch, id=id)
        batch_name = batch.name
        batch.delete()
        messages.success(request,f"Batch <strong>{batch_name}</strong> deleted successfully.")
    except Exception as e:
        print(e)
        messages.success(request,f"NOt deleted ")
    return redirect('ViewBatches')
    



    
# UpdateBatch
def UpdateBatch(request,id):
    batch = get_object_or_404(Batch, id=id)

    if request.method == "POST":
        # --- PROCESS FORM SUBMISSION ---
        
        # 1. Get data from request.POST
        name = request.POST.get("name")
        course_id = request.POST.get("course")
        instructor_id = request.POST.get("instructor")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        print(f"update batch start date{start_date}")
        status = request.POST.get("status")

        # 2. Update Basic Fields
        batch.name = name
        batch.start_date = start_date
        batch.end_date = end_date
        batch.status = status

        # 3. Handle Foreign Keys
        # Course (Required)
        if course_id:
            batch.course = get_object_or_404(Course, id=course_id)
        
        # Instructor (Optional / Nullable)
        if instructor_id:
            batch.instructor = get_object_or_404(Instructor, id=instructor_id)
        else:
            # If empty string was sent (User selected "No Instructor")
            batch.instructor = None
        #validation for date 
        if not (start_date and end_date):
            messages.error(request,"You must provide start date and end date ")
            return redirect('UpdateBatch',id)
        if start_date>end_date:
            messages.error(request,"Start date should be before end date:")
            return redirect('UpdateBatch',id)

        # 4. Save to Database
        batch.save()
        messages.success(request, "Batch updated successfully!")
        return redirect('ViewBatches') 

    else:
        start = batch.start_date.strftime('%Y-%m-%d') if batch.start_date else ''
        end = batch.end_date.strftime('%Y-%m-%d') if batch.end_date else ''
        # --- RENDER FORM (GET REQUEST) ---
        
        courses = get_list_or_404(Course)
        instructors = get_list_or_404(Instructor)

        # We must format dates as YYYY-MM-DD for HTML input type="date"
        # If dates are None, we pass empty strings
        

        context = {
            "batch": batch,
            "courses": courses,
            "instructors": instructors,
            
            # Context variables specifically for your Template Logic:
            "selected_course": batch.course.id,
            
            # check if instructor exists before accessing .id to avoid errors
            "selected_instructor": batch.instructor.id if batch.instructor else None,
            
            "start_date": start,
            "end_date": end,
            "current_status": batch.status, 
        }

        return render(request, "ADMIN/BATCH/Update-Batch.html", context)

# -----Instructor-------
def Instructor1(request):
    instructors=None
    # extract instructors from the DB
    try:
        data=get_list_or_404(Instructor)
        instructors=data
    except:
        messages.error(request,"No data have been found")  
    context = {
        'instructors': instructors
        }

    return render(request,'ADMIN/Instructor/View-Instructor.html',context)
# UpdateInstructor
def UpdateInstructor(request,id):
    return render(request,'ADMIN/Instructor/Update-Instructor.html')
# DeleteInstructor
def DeleteInstructor(request,id):
    try:
        instructor=get_object_or_404(Instructor,id=id)
        instructor.delete()
        messages.error(request,f"The instructor <strong>{instructor.user.username}</strong> is deleted from the DB")
    except:
        messages.error(request,f"instructor not found")

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
