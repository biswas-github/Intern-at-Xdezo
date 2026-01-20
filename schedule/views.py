from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.contrib import messages
from App.models import Schedule,Instructor,Batch,Classroom
from datetime import timedelta

# Create your views here.
#-------Schedule 
# ViewSchedule
def ViewSchedule(request):
    import datetime
    today = datetime.date.today()
    schedules=[]
    instructors=[]
    try:
        schedules = get_list_or_404(
        Schedule.objects.select_related('batch', 'classroom', 'instructor').order_by('-date'))
        
    except:
        messages.error(request,"No data found !")

    # 2. Fetch instructors for the filter dropdown (optional, but needed for your UI)
    try:
        instructors = get_list_or_404(Instructor.objects.all())
    except:
        messages.error(request,"No instructor found !")

    context = {
        'schedules': schedules,
        'instructors': instructors
    }
    return render(request, 'ADMIN/Schedule/View-Schedule.html', context)


# DeleteSchedule
def DeleteSchedule(request,id):
    try:
        sched=get_object_or_404(Schedule,id=id)
        if sched:
            s_date=sched.date
            s_time=sched.start_time
            s_batch=sched.batch.name
            sched.delete()
            messages.success(request,f"Schedule Deleted fron the DB date :{s_date}  time: {s_time} batch: {s_batch}")
    except Exception as e:
        messages.error(request,"Data cant be deleted ")
        print(e)
    return render(request,'ADMIN/Schedule/Delete-Schedule.html')
# AddSchedule
def AddSchedule(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')

        try:
            # 1. Fetch the Batch immediately (We need it for both Recurring and Single)
            batch_id = request.POST.get('batch')
            batch = get_object_or_404(Batch, id=batch_id)

            # 2. Determine the Instructor
            # Logic: If form has instructor -> Use it.
            #        Else if Batch has instructor -> Use Batch's instructor.
            #        Else -> None.
            form_instructor_id = request.POST.get('instructor')
            
            final_instructor_id = None

            if form_instructor_id:
                # User manually selected an instructor (Overrides batch default)
                final_instructor_id = form_instructor_id
            elif hasattr(batch, 'instructor') and batch.instructor:
                # User left it blank, but Batch has a default instructor assigned
                final_instructor_id = batch.instructor.id

            # 3. Clean Classroom Data
            classroom_id = request.POST.get('classroom')
            if not classroom_id: 
                classroom_id = None

           
            if form_type == 'recurring':
                # Get days as integers (Match your HTML value="0" to Python's 0)
                selected_days = [int(d) for d in request.POST.getlist('days')]
                
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')

                if not batch.start_date or not batch.end_date:
                    raise ValueError("Batch does not have valid Start/End dates.")

                schedules_to_create = []
                current_date = batch.start_date

                while current_date <= batch.end_date:
                    # Check if current day (0=Mon...6=Sun) matches user selection
                    if current_date.weekday() in selected_days:
                        schedules_to_create.append(
                            Schedule(
                                batch=batch,
                                date=current_date,
                                start_time=start_time,
                                end_time=end_time,
                                # Uses Form or Batch default
                                instructor_id=final_instructor_id, 
                                classroom_id=classroom_id,
                                status='SCHEDULED'
                            )
                        )
                    current_date += timedelta(days=1)

                if schedules_to_create:
                    Schedule.objects.bulk_create(schedules_to_create)
                    messages.success(request, f"Generated {len(schedules_to_create)} sessions. (Instructor: {Instructor.objects.get(id=final_instructor_id).full_name or 'TBA'})")
                else:
                    messages.warning(request, "No dates matched within the batch duration.")
                
                return redirect('ViewSchedule')

         
            elif form_type == 'single':
                date_val = request.POST.get('date')
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                status_val = request.POST.get('status')

                Schedule.objects.create(
                    batch=batch,
                    date=date_val,
                    start_time=start_time,
                    end_time=end_time,
                    instructor_id=final_instructor_id, # Uses Form or Batch default
                    classroom_id=classroom_id,
                    status=status_val
                )
                
                messages.success(request, "Single session added successfully!")
                return redirect('ViewSchedule')

        except Exception as e:
            messages.error(request, f"Error: {e}")

    # --- GET REQUEST ---
    try:
        # Use get_list_or_404 for batches (as requested)
        batches = get_list_or_404(Batch)
        
        # Keep .all() for these so page doesn't crash if empty
        instructors = Instructor.objects.all()
        classrooms = Classroom.objects.all()
    except:
        batches = []
        instructors = []
        classrooms = []
        messages.warning(request, "No Batches found. Please create a Batch first.")

    context = {
        'batches': batches,
        'instructors': instructors,
        'classrooms': classrooms
    }
    return render(request, 'ADMIN/Schedule/Add-Schedule.html', context)


# EditSchedule
def EditSchedule(request,id):
    schedule = get_object_or_404(Schedule, id=id)

    if request.method == "POST":
        try:
            # 2. Extract Data
            batch_id = request.POST.get('batch')
            date_val = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            status_val = request.POST.get('status')
            
            # Special handling for Optional Fields (Instructor/Classroom)
            # If value is an empty string "", we must set it to None (Null)
            instructor_id = request.POST.get('instructor') or None
            classroom_id = request.POST.get('classroom') or None

            # 3. Update Object Fields
            schedule.batch_id = batch_id
            schedule.date = date_val
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.status = status_val
            schedule.instructor_id = instructor_id
            schedule.classroom_id = classroom_id

            # 4. Save Changes
            schedule.save()

            messages.success(request, "Schedule updated successfully!")
            return redirect('ViewSchedule')

        except Exception as e:
            messages.error(request, f"Error updating schedule: {e}")
            return redirect('ViewSchedule')

    # --- GET REQUEST ---
    # Fetch lists for the dropdowns
    batches = Batch.objects.all()
    instructors = Instructor.objects.all()
    classrooms = Classroom.objects.all()

    context = {
        'schedule': schedule,
        'batches': batches,
        'instructors': instructors,
        'classrooms': classrooms
    }
    return render(request, 'ADMIN/Schedule/Edit-Schedule.html', context)

# FreeRoom
def FreeRoom(request):
    free_rooms = []

    # Get data from URL
    user_date = request.GET.get('date')
    user_start = request.GET.get('start_time')
    user_end = request.GET.get('end_time')

    if user_date and user_start and user_end:
        try:
            # --- STEP 1: Find schedules that conflict ---
            # "Find schedules on this date where time overlaps"
            busy_schedules = Schedule.objects.filter(
                date=user_date,
                status='SCHEDULED',
                start_time__lt=user_end, # Starts before we finish
                end_time__gt=user_start  # Ends after we start
            )

            # --- STEP 2: Create a list of Busy Room IDs ---
            # We loop through the schedules and write down the Room ID in a list.
            busy_ids = []
            for schedule in busy_schedules:
                # Check if a classroom is assigned to avoid errors
                if schedule.classroom:
                    busy_ids.append(schedule.classroom.id)
            
            # Example result: busy_ids = [1, 5]


            # --- STEP 3: Check every room one by one ---
            # Get all active rooms
            all_rooms = Classroom.objects.filter(is_active=True)

            # Loop through every room in the school
            for room in all_rooms:
                # If the room's ID is NOT in our busy list, it is free!
                if room.id not in busy_ids:
                    free_rooms.append(room)

        except Exception as e:
            print(e)
            messages.error(request, "Error searching.")

    context = {
        'free_rooms': free_rooms
    }
    return render(request, 'ADMIN/Schedule/Free-Room.html', context)
