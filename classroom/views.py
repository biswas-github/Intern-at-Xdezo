from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from App.models import Classroom
from django.contrib import messages

# Create your views here.
#------Classroom----#
# ViewClassroom
def ViewClassroom(request):
    classrooms=[]
    try:
        classrooms=get_list_or_404(Classroom.objects.order_by('-id'))
    except Exception as e:
        print(f"Error is {e}")
        messages.error(request,"No data found in the DB")
        
    
    context={
        "classrooms":classrooms}
    return render(request,'ADMIN/Classroom/View-Classroom.html',context)
# addclassroom 
def AddClassroom(request):
     if request.method=="POST":
        try:
            class_name=request.POST.get('name')
            capacity=request.POST.get('capacity')
            is_active=request.POST.get('is_active')
            if is_active=="True":
                is_active=True
            else:
                is_active=False
        except:
            messages.error(request,"Data Extration from the form is Unsuccessful !")
            return redirect('ViewClassroom')
        try:
            Classroom.objects.create(
                name=class_name,
                capacity=capacity,
                is_active=is_active
            )
            messages.success(request,f" <strong>{ class_name }</strong> saved to the DB")
            return redirect('ViewClassroom')
        except Exception as e:
            print("error is ",e)
            messages.error(request,"Data NOT Saved to the DB")
            return redirect('AddClassroom')
            
     return render(request,'ADMIN/Classroom/Add-Classroom.html')
# update classroom
def UpdateClassroom(request,id):
    if request.method == "POST":
        context={}
        try:
            # 1. Retrieve the existing object
            classroom = get_object_or_404(Classroom, id=id)
            
            # 2. Extract data from the form
            name = request.POST.get('name')
            capacity = request.POST.get('capacity')
            is_active_val = request.POST.get('is_active') # Returns string "True" or "False"

            # 3. Update the fields
            classroom.name = name
            classroom.capacity = capacity
            
            # 4. Handle Boolean conversion 
            # (HTML sends "True"/"False" as strings, Python needs booleans)
            if is_active_val == "True":
                classroom.is_active = True
            else:
                classroom.is_active = False

            # 5. Save the changes to the database
            classroom.save()

            messages.success(request, "Classroom updated successfully!")
            return redirect('ViewClassroom') # Change this to your actual list view name

        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")
            # Optional: redirect back to the edit page or list page on error

    if request.method=="GET":
        context={}
        try:
            classroom=get_object_or_404(Classroom,id=id)
            context={
                "name":classroom.name,
                "capacity":classroom.capacity,
                "is_active":classroom.is_active
            }
            
        except:
            messages.error(request,"NO classroom found")
     
    return render(request,'ADMIN/Classroom/Update-Classroom.html',context)
# DeleteClassroom
def DeleteClassroom(request,id):
    try:
        classroom=get_object_or_404(Classroom,id=id)
        classroom.delete()
        messages.success(request,"The classroom is Deleted ")
    except Exception as e:
        print(f"error while deleting :{e}")
        messages.success(request,"The classroom couldn't be Deleted ")
        return redirect('ViewClassroom')
        
    
    return render(request,'ADMIN/Classroom/Delete-Classroom.html')
