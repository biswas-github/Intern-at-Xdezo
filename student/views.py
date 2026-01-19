from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib import messages
from App.models import Student
# Create your views here.


# DataManagement-Student for managing the students 
# add the student
def DataManagementStudent(request):
    if request.method=='POST':
        print("post method has hit")
    
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
        except ValueError as v:
            messages.error(request, "Student name should not contain special chracters  !")

        except Exception as e :
            # Other exceptions
            print(f"cant be done{e}")
            messages.error(request, "Student cant be added !")
    return render(request,'ADMIN/DataManagement_Student.html')


    
# to view all the students
def ViewStudent(request):
    try:
        student = Student.objects.order_by('-id')
        student=get_list_or_404(Student.objects.order_by('-id'))
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
    except:
        students=[]
        messages.error(request,"No student found !") 

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
        messages.success(request,"student deleted")
        # deleted
    except Exception as e:
        print("not deleted error {e}")
       
    return render(request,'ADMIN/Delete-Student.html')
