from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.contrib import messages
from App.models import Course,Instructor,Batch
import datetime

# Create your views here.


# ----Batch------#
from datetime import datetime
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
                        "name":instructor.full_name
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
        batches = get_list_or_404(Batch.objects.select_related(
        'course',
        'instructor',
        ).order_by('-id'))
    except:
        batches=[]
        messages.error(request,"No data Found ")
        
    
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
