from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.contrib import messages
from App.models import Instructor

# Create your views here.



# -----Instructor-------
def Instructor1(request):
    instructors=None
    # extract instructors from the DB
    try:
        data=get_list_or_404(Instructor.objects.order_by("-id"))
        instructors=data
    except:
        messages.error(request,"No data have been found")  
    context = {
        'instructors': instructors
        }

    return render(request,'ADMIN/Instructor/View-Instructor.html',context)
# UpdateInstructor
def UpdateInstructor(request,id):
    if request.method=="GET":
        context={}
        try:
            instrutor_details=get_object_or_404(Instructor,id=id)
            name=instrutor_details.full_name.split(" ")
            first_name=name[0]
            last_name=name[1]
            context={
                "first_name":first_name,
                "last_name":last_name,
                "email":instrutor_details.email,
                "address":instrutor_details.address,
                "phone":instrutor_details.phone,
                "specialization":instrutor_details.specialization,
                "status":instrutor_details.is_active,
                "bio":instrutor_details.bio
            }
            print(context["status"])
        except Exception as e:
            print(e)
        return render(request,'ADMIN/Instructor/Update-Instructor.html',context)
    if request.method=="POST":
        try:
            instructor=get_object_or_404(Instructor,id=id)
        except:
            messages.error(request,"Data not found")
            return redirect('Instructor')
           

        try:
             # extract information from the Form
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            full_name=first_name+ " " +last_name

            email=request.POST.get('email')
            phone=request.POST.get('phone')
            address=request.POST.get('address')
            specialization=request.POST.get('specialization')
            is_active=request.POST.get('is_active')
            bio=request.POST.get('bio')

        except Exception as e:
            print("error is ", e)
            messages.error(request,"data fetching error from the form ")
            return redirect('UpdateInstructor',id)
        try:
            # in models : is_active is boolean 
            # so we make it boolean 
            if is_active=="is_active":
                is_active=True
            else:
                is_active=False
            # after extracting the data from the form updating the DB
            instructor.full_name=full_name
            instructor.email=email
            instructor.phone=phone
            instructor.address=address
            instructor.specialization=specialization
            instructor.is_active=is_active
            instructor.bio=bio
            # save
            instructor.save()
            print("saved ")
            messages.success(request,f"the instructor <strong>{first_name}</strong>Updated Successfully ")
            return redirect('Instructor')
        except Exception as e:
            messages.error(request,"Data cant be Saved  ")
            return redirect('UpdateInstructor',id)

# DeleteInstructor
def DeleteInstructor(request,id):
    try:
        instructor=get_object_or_404(Instructor,id=id)
        full_name=instructor.full_name
        instructor.delete()
        messages.success(request,f"The instructor <strong>{full_name}</strong> is deleted from the DB")
    except:
        messages.error(request,f"instructor not found")

    return render(request,'ADMIN/Instructor/Delete-Instructor.html')
# AddInstructor
def AddInstructor(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        full_name=first_name+ " " +last_name

        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        specialization=request.POST.get('specialization')
        is_active=request.POST.get('is_active')
        bio=request.POST.get('bio')
        if is_active=="is_active":
            is_active=True
        else:
            is_active=False

        try:
            Instructor.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                specialization=specialization,
                is_active=is_active,
                bio=bio
                )
            messages.success(request,f"Instructor <strong>{full_name}</strong> has been Added Successfully ")
            return redirect('Instructor') 
        except Exception as e:
            print(e)
            messages.error(request,"Sorry, Instructor can't be added !")

    return render(request,'ADMIN/Instructor/Add-Instructor.html')
