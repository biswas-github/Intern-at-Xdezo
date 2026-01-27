from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

# Student model
class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        COMPLETED = "COMPLETED", "Completed"
        DROPPED = "DROPPED", "Dropped"

    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        
        name = self.full_name
        
        # Check  Length
        if len(name) <= 4:
            raise ValueError("Name validation failed: Must be longer than 4 characters.")
        
        # Check  Special Characters
        # We check if the name contains anything that ISN'T a letter or a space.
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" + " "
        for char in name:
            if char not in allowed_chars:
                raise ValueError("Name validation failed: Cannot contain special characters (only letters and spaces allowed).")


        #  Phone Number Validation (10 digits starting from 98) 
        phone_number = self.phone
        
        # Only validate if a phone number is provided (since field is blank/null allowed)
        if phone_number:
            # Check  Length is exactly 10
            if len(phone_number) != 10:
                raise ValueError("Phone validation failed: Must be exactly 10 digits.")
            
            #  Starts with "98"
            # if not phone_number.startswith("98"):
            #     raise ValueError("Phone validation failed: Must start with '98'.")
            
            # Check 2c: Entirely digits (basic check)
            if not phone_number.isdigit():
                 raise ValueError("Phone validation failed: Must only contain digits.")

        super().save(*args, **kwargs)

# ADDing the courses for the System 
# includes course info such as : tilttle , course code , description,
class Course(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    # default_duration_weeks : how l0ng the course usally runs 
    default_duration_weeks = models.PositiveIntegerField(blank=True, null=True)
    Course_fee = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.code} - {self.title}"

# Instructor 
class Instructor(models.Model):
    # 1 to 1 with the user model for the instructor
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True) # distinct email for every instructor
    phone = models.CharField(max_length=20) 
    address = models.TextField(blank=True, null=True)
    
    specialization = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # It is always good practice to keep an active flag for soft deletes
    is_active = models.BooleanField(default=True)
    
    # Optional: Track when they were added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)


    def __str__(self):
        return self.full_name
    
from colorfield.fields import ColorField
# There could be many(running classes ) batch for a single courses so we need to do the Batch 
class Batch(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "UPCOMING", "Upcoming"
        ONGOING = "ONGOING", "Ongoing"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
# a course has many batches 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_batches")
    # name of that batch Batch 1 , 2 
    # Example  "Python Jan 2026 Morning", "Python Jan 2026 Evening"
    name = models.CharField(max_length=150)  
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructor_batches",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING,
    )
    color = ColorField(default="#124470")  # NEW FIELD

    def __str__(self):
        return f"{self.course.code} - {self.name}"

# Student are enrolled and thy can enroll on many batch but only once in a Single batch
class Enrollment(models.Model):
    # status of the enrollment in the courses 
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        DROPPED = "DROPPED", "Dropped"

    # student 
    student = models.ForeignKey(Student, on_delete=models.SET_NULL,null=True, related_name="student_enrollments")
    # related batch
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL,null=True, related_name="batch_enrollments")
    enrolled_on = models.DateField(auto_now_add=True)


    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE, # by default the enrollment is active 
    )

    class Meta:
        # 1 student can enroll once in a batch
        unique_together = ("student", "batch")

    def __str__(self):
        return f"{self.student} -> {self.batch}"


# Adding the classrooms 
class Classroom(models.Model):
    # e.g. "Room 101"
    name = models.CharField(max_length=100)  
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

# Adding the Schudules 
# Scheduling the classroom, instructors ,batch , date , start and end times  
class Schedule(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="sessions")
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="classroom_sessions",
    )
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructor_sessions",
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
   
       

    def __str__(self):
        return f"{self.batch} @ {self.date} {self.start_time}-{self.end_time}"
    

    # validation and conflits  are checked here 
    def clean(self):
        # This is the "Checking" phase
       
    #classroom conflits
    # at the time , on that day the classroom is occupied or not . 
    # if occupied then raise validation error 
        if self.classroom:  # Skip if no room selected
            existing = Schedule.objects.filter(
                classroom=self.classroom,
                date=self.date,
                status='SCHEDULED'
            ).exclude(pk=self.pk).filter(
                # Time overlap check (simple version)
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
            if existing.exists():
                conflict=existing.first()
                raise ValidationError(f"The class  {self.classroom.name} is busy on the {self.start_time} with {conflict.start_time}--{conflict.end_time}")
    # Instructor validation 

    #   check if the instructor is busy or not at the given date , given time 
    # it checks for if the instructor conflits on the given time 
    # because the instructor may be teaching other batches  
        if self.instructor:
            existing = Schedule.objects.filter(
                instructor=self.instructor,
                date=self.date,
                status='SCHEDULED'
            ).exclude(pk=self.pk).filter(
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
            if existing.exists():
                conflict = existing.first()
                raise ValidationError(
                    f"Instructor {self.instructor.full_name} busy at this time on the batch {conflict.batch.name}"
                )
            

    # Check for the Batch --> check wether the batch is already scheduled already at that given time 
        existing = Schedule.objects.filter(
            batch=self.batch,
            date=self.date,
            start_time=self.start_time,
            end_time=self.end_time,
            status='SCHEDULED'
        ).exclude(pk=self.pk)
        
        if existing.exists():
            raise ValidationError("This batch already has class at this time !")

        # check for batch start date and end date 
        if not self.batch.start_date or not self.batch.end_date:
                     raise ValueError("Selected Batch does not have valid Start/End dates.")


    def save(self, *args, **kwargs):
        # 1. Start the inspection
        self.full_clean()
        # 2. If the inspection passed, do the action
        super().save(*args, **kwargs)


# Choosing the method for the Payments in the database 
class Payments(models.Model):
    class Method(models.TextChoices):
        ESEWA = 'ESEWA', 'ESEWA'
        BANK = 'BANK', 'BANK'
        CASH = 'CASH', 'CASH'
        OTHERS = 'OTHERS', 'OTHERS'

    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        related_name='student_payments',
    )
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enrollment_payments',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(
        max_length=10,
        choices=Method.choices,
        default=Method.CASH,
    )
    remarks = models.TextField(blank=True, null=True)
    ref_no=models.CharField(blank=True , null=True)

    def __str__(self):
        return f"{self.student} - {self.amount} on {self.date.date()}"

# Export history of the information
class ExportHistory(models.Model):
    class ExportType(models.TextChoices):
        STUDENTS = "STUDENTS", "Students"
        COURSES = "COURSES", "Courses"
        BATCHES = "BATCHES", "Batches"
        ENROLLMENTS = "ENROLLMENTS", "Enrollments"
        PAYMENTS = "PAYMENTS", "Payments"
        SCHEDULES = "SCHEDULES", "Schedules"
        INSTRUCTORS = "INSTRUCTORS", "Instructors"
        CLASSROOMS = "CLASSROOMS", "Classrooms"
        ATTENDANCE = "ATTENDANCE", "Attendance"

    export_type = models.CharField(
        max_length=20,
        choices=ExportType.choices,
    )

    exported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exports",
    )
    exported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.export_type} export by {self.exported_by} at {self.exported_at}"
