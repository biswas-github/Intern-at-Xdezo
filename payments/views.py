from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from App.models import Payments,Student,Enrollment
from django.contrib import messages
from django.db.utils import IntegrityError
# django.core.exceptions.ValidationError
from django.core.exceptions import ValidationError
from datetime import datetime,date


# Create your views here.

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from decimal import Decimal

def AddPayment(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        enrollment_id = request.POST.get('enrollment')
        method = request.POST.get('method')
        ref_no = request.POST.get('ref_no')
        remarks = request.POST.get('remarks')
        print(enrollment_id)
        print(ref_no)
        try:
            amount = Decimal(request.POST.get('amount'))
            if amount <= 0:
                raise ValueError
        except:
            messages.error(request, "Please enter a valid amount.")
            return redirect("AddPayment")
        print(enrollment_id)
        if enrollment_id:
            print(enrollment_id)
            enrollment_obj = get_object_or_404(Enrollment, id=enrollment_id)
            student_obj = enrollment_obj.student

            if not student_obj or student_obj is None:
                messages.warning(request, "Student linked to enrollment no longer exists.")
                return redirect("AddPayment")

        else:
            if not student_id:
                messages.error(request, "Please select a student or an enrollment.")
                return redirect("AddPayment")

            student_obj = get_object_or_404(Student, id=student_id)
            enrollment_obj = None

        with transaction.atomic():
            Payments.objects.create(
                student=student_obj,
                enrollment=enrollment_obj,
                amount=amount,
                method=method,
                ref_no=ref_no,
                remarks=remarks
            )

        messages.success(
            request,
            f"Payment of Rs. {amount} added successfully for {student_obj.full_name}."
        )
        return redirect('ViewPayment')

    # GET
    students = Student.objects.all().order_by('-id')
    enrollments = Enrollment.objects.all()


    return render(request, 'ADMIN/Payment/Add-Payment.html', {
        'students': students,
        'enrollments': enrollments,
    })


#   UpdatePayment
def UpdatePayment(request, id):
    payment = get_object_or_404(Payments, id=id)

    if request.method == 'POST':
        student_id = request.POST.get('student')
        enrollment_id = request.POST.get('enrollment')
        amount = Decimal(request.POST.get('amount'))
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
        course_fee = e.batch.course.Course_fee if e.batch else "batch deleted or not found"
        batch_start_date = e.batch.start_date if e.batch else "batch deleted or not found"

        # Sum payments only for this enrollment (ignore "general payments")
        paid_all = (
            Payments.objects
            .filter(enrollment=e))  
        sum=0              # only enrollment payment
        for data in paid_all:
            sum+=data.amount
        paid=sum

        due=0
        if due:
            due = int(course_fee) - int(paid)
        else:
            continue
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

