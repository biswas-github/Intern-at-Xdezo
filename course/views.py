from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.contrib import messages
from App.models import Course

# Create your views here.
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
        from App.models import Course
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

