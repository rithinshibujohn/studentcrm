from django.contrib import admin
from .models import Student,Course,CourseEnrollment,EducationDetail,Subject,Topic

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "course",
        "created_at",
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
admin.site.register(Topic)