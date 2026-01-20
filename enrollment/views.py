from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from App.models import Enrollment,Student,Batch
from django.contrib import messages
from django.db.utils import IntegrityError

# Create your views here.
#------------ViewEnrollment--------------#
from django.shortcuts import render
from django.contrib import messages

def ViewEnrollment(request):
    enrollments = []

    enroll1 = Enrollment.objects.order_by('-id')

    if not enroll1:
        messages.error(request, "Data not found!")

    data = []
    for enroll in enroll1:
        data.append({
            "id": enroll.id,
            "student_name": enroll.student.full_name if enroll.student else "student deleted",
            "batch_name": enroll.batch.name if enroll.batch else "no batch/batch deleted",
            "enrolled_date": enroll.enrolled_on,
            "status": enroll.status,
        })

    enrollments = data

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
