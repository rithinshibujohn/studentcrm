from django.conf import settings
from django.db import models
import uuid


class Student(models.Model):
    student_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    address = models.TextField()
    course = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="students/")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students_created"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students_updated"
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.name


class EducationDetail(models.Model):
    education_detail_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="education_details"
    )
    qualification = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="education_details_created"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="education_details_updated"
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.student.name} - {self.qualification}"


class Course(models.Model):
    course_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_months = models.PositiveIntegerField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses_created"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses_updated"
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.name


class CourseEnrollment(models.Model):
    course_enrollment_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="course_enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="enrollments"
    )
    start_date = models.DateField()
    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="course_enrollments_created"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="course_enrollments_updated"
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"


class Subject(models.Model):
    subject_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subjects_created"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subjects_updated"
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Topic(models.Model):
    topic_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="topics"
    )
    name = models.CharField(max_length=200)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="topics_created"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="topics_updated"
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.name