from django.urls import path
from student_crm import settings
from . import views



urlpatterns = [
    path("", views.StudentListView.as_view(), name="student_list"),
    path("add/", views.StudentCreateView.as_view(), name="student_add"),
    path("courses/",views.CourseListView.as_view(), name="course_list"),
    path("courses/add/",views.CourseCreateView.as_view(),name="course_add"),
    path("<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_edit"),
    path("<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("courses/<int:pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("courses/<int:pk>/delete/",views.CourseDeleteView.as_view(),name="course_delete"),
    path("upload/", views.upload_students, name="upload_students"),
    path("pdf/", views.download_pdf, name="download_pdf"),
]
