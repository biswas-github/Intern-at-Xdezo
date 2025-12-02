from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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
    date_of_birth = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

# ADDing the courses for the System 
# includes course info such as : tilttle , course code , description,
class Course(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    # default_duration_weeks : how ling the course usally runs 
    default_duration_weeks = models.PositiveIntegerField(blank=True, null=True)
    Course_fee = models.DecimalField(
        max_digits=10,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.code} - {self.title}"


# There could be many(running classes ) batch for a single courses so we need to do the Batch 
class Batch(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "UPCOMING", "Upcoming"
        ONGOING = "ONGOING", "Ongoing"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
# a course has many batches 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="batches")
    # name of that batch Batch 1 , 2 
    # Example  "Python Jan 2026 Morning", "Python Jan 2026 Evening"
    name = models.CharField(max_length=150)  
    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="batches",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING,
    )

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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    # related batch
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="enrollments")
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
