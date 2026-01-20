from django.shortcuts import render
from datetime import datetime

# Create your views here.
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
