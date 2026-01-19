from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404,get_list_or_404
from django.http import HttpResponse,Http404
from datetime import date
# time delta is used for incrementting or decrement by some days 
# eg:  # Move to next day
# current_date += timedelta(days=1)
from datetime import timedelta
from django.contrib import messages
from App.models import Course,Instructor,Batch,Classroom,Schedule,Payments
from django.db import IntegrityError
from django.core.exceptions import ValidationError


#  ViewSystemUser
from datetime import datetime, timedelta
def ViewSystemUser(request):
      # In a real model, you don't need this helper, the template calls user.get_full_name
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