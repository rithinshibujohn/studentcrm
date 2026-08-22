from django.urls import path
from student_crm import settings
from . import views



urlpatterns = [
    path("", views.StudentListView.as_view(), name="student_list"),
    path("add/", views.StudentCreateView.as_view(), name="student_add"),
    path("courses/",views.CourseListView.as_view(), name="course_list"),
    path("courses/add/",views.CourseCreateView.as_view(),name="course_add"),
    path("certificates/templates/",views.CertificateTemplateListView.as_view(),name="certificate_template_list",),
    path("certificates/templates/add/",views.CertificateTemplateCreateView.as_view(),name="certificate_template_add",),
    path("certificates/student-enrollments/",views.get_student_enrollments,name="get_student_enrollments",),
    path("certificates/generate/",views.CertificateCreateView.as_view(),name="certificate_generate",),
    path("certificates/<uuid:pk>/edit-content/",views.CertificateContentEditView.as_view(), name="certificate_edit_content",),
    path("certificates/<uuid:pk>/preview/",views.CertificatePreviewView.as_view(),name="certificate_preview",),
    path("certificates/<uuid:pk>/download/",views.certificate_pdf_download,name="certificate_pdf_download",),
    path("certificates/templates/<uuid:pk>/edit/", views.CertificateTemplateUpdateView.as_view(), name="certificate_template_edit",),
    path("certificates/templates/<uuid:pk>/delete/", views.CertificateTemplateDeleteView.as_view(), name="certificate_template_delete",),
    path("<uuid:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("<uuid:pk>/edit/", views.StudentUpdateView.as_view(), name="student_edit"),
    path("<uuid:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("courses/<uuid:pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("courses/<uuid:pk>/delete/",views.CourseDeleteView.as_view(),name="course_delete"),
    path("upload/", views.upload_students, name="upload_students"),
    path("pdf/", views.download_pdf, name="download_pdf"),
]
