from django.contrib import admin
from .models import Certificate, Student,Course,CourseEnrollment,EducationDetail,Subject,Topic

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "course",
        "created_date",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "course",
    )

    list_filter = (
        "gender",
        "course",
    )

admin.site.register(Course)
admin.site.register(CourseEnrollment)
admin.site.register(EducationDetail)
admin.site.register(Subject)
admin.site.register(Certificate)

