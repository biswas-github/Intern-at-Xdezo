from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

# Import your models
from App.models import Student, Batch, Schedule, Payments, Classroom, Enrollment, Course

# ==========================================
# 1. HELPER FUNCTION (Classroom Logic)
# ==========================================
def classroom_block():
    """
    Fetches active classrooms and their schedules for TODAY.
    Returns a list of dictionaries to be used in the Modal.
    """
    today = timezone.now().date()
    classrooms_data = []

    # Get all active classrooms
    classrooms = Classroom.objects.filter(is_active=True)

    for room in classrooms:
        sessions_list = []

        # Get today's schedules for this specific room
        # select_related fetches Batch and Instructor details in 1 query (Fast!)
        schedules = Schedule.objects.filter(
            classroom=room,
            date=today,
            status=Schedule.Status.SCHEDULED
        ).select_related('batch', 'instructor')

        for sched in schedules:
            sessions_list.append({
                "start": sched.start_time.strftime("%H:%M"),
                "end": sched.end_time.strftime("%H:%M"),
                
                # Use the new ColorField or fallback to grey
                "batch_color": sched.batch.color if sched.batch else "#6c757d", 
                
                "batch": sched.batch.name if sched.batch else "No Batch",
                "instructor": sched.instructor.full_name if sched.instructor else "TBA",
            })

        # Append this room's data to the main list
        classrooms_data.append({
            "name": room.name,
            "capacity": room.capacity,
            "sessions": sessions_list
        })
    
    return classrooms_data
