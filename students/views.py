from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import CourseEnrollment, Student, Course, Subject,Topic, CertificateTemplate,Certificate
from .forms import (
    StudentForm,
    EducationDetailFormSet,
    CourseEnrollmentFormSet,
    StudentForm,
    CourseForm,
    SubjectForm,    
    SubjectFormSet,
    CourseFormSet,
    TopicFormSet,
    CertificateTemplateForm,
    CertificateForm,
)
from django.db import transaction
from .utils import import_students_from_excel
from .excel_form import ExcelUploadForm
from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
from .pdf import generate_student_pdf
from django.db import transaction
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.utils.html import escape
from django.contrib.staticfiles import finders
from django.conf import settings
from playwright.sync_api import sync_playwright
import base64
import mimetypes

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"


class StudentCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("student_list")
    success_message = "Student added successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["education_formset"] = EducationDetailFormSet(
                self.request.POST,
                instance=self.object,
                prefix="education"
            )

            context["enrollment_formset"] = CourseEnrollmentFormSet(
                self.request.POST,
                instance=self.object,
                prefix="enrollment"
            )
        else:
            context["education_formset"] = EducationDetailFormSet(
                instance=self.object,
                prefix="education"
            )

            context["enrollment_formset"] = CourseEnrollmentFormSet(
                instance=self.object,
                prefix="enrollment"
            )

        return context

    def form_valid(self, form):

        education_formset = EducationDetailFormSet(
            self.request.POST,
            instance=self.object,
            prefix="education"
        )

        enrollment_formset = CourseEnrollmentFormSet(
            self.request.POST,
            instance=self.object,
            prefix="enrollment"
        )

        if (
            education_formset.is_valid()
            and enrollment_formset.is_valid()
        ):
            with transaction.atomic():

                self.object = form.save()

                education_formset.instance = self.object
                education_formset.save()

                enrollment_formset.instance = self.object
                enrollment_formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)


class StudentUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("student_list")
    success_message = "Student updated successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["education_formset"] = EducationDetailFormSet(
                self.request.POST,
                instance=self.object,
                prefix="education"
            )

            context["enrollment_formset"] = CourseEnrollmentFormSet(
                self.request.POST,
                instance=self.object,
                prefix="enrollment"
            )
        else:
            context["education_formset"] = EducationDetailFormSet(
                instance=self.object,
                prefix="education"
            )

            context["enrollment_formset"] = CourseEnrollmentFormSet(
                instance=self.object,
                prefix="enrollment"
            )

        return context

    def form_valid(self, form):

        education_formset = EducationDetailFormSet(
            self.request.POST,
            instance=self.object,
            prefix="education"
        )

        enrollment_formset = CourseEnrollmentFormSet(
            self.request.POST,
            instance=self.object,
            prefix="enrollment"
        )

        print("STUDENT ERRORS:", form.errors)
        print("EDUCATION ERRORS:", education_formset.errors)
        print(
            "EDUCATION NON-FORM ERRORS:",
            education_formset.non_form_errors()
        )
        print("ENROLLMENT ERRORS:", enrollment_formset.errors)
        print(
            "ENROLLMENT NON-FORM ERRORS:",
            enrollment_formset.non_form_errors()
        )

        if (
            education_formset.is_valid()
            and enrollment_formset.is_valid()
        ):
            with transaction.atomic():

                self.object = form.save()

                education_formset.instance = self.object
                education_formset.save()

                enrollment_formset.instance = self.object
                enrollment_formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)


class StudentDeleteView(LoginRequiredMixin,
                        DeleteView):

    model = Student
    template_name = "students/student_confirm_delete.html"

    success_url = reverse_lazy("student_list")

    def form_valid(self, form):
        messages.success(self.request, "Student deleted successfully.")
        return super().form_valid(form)


class StudentDetailView(LoginRequiredMixin,
                        DetailView):

    model = Student
    template_name = "students/student_detail.html"



def upload_students(request):

    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            import_students_from_excel(request.FILES["file"])
            messages.success(request, "Students imported successfully.")
            return redirect("student_list")

    else:
        form = ExcelUploadForm()

    return render(
        request,
        "students/upload_excel.html",
        {"form": form},
    )


def download_pdf(request):

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        'attachment; filename="students.pdf"'
    )

    generate_student_pdf(response)

    return response

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "students/course_list.html"
    context_object_name = "courses"


class CourseCreateView(LoginRequiredMixin, View):
    template_name = "students/course_form.html"

    def get(self, request):
        course_formset = CourseFormSet(
            prefix="courses"
        )

        return render(
            request,
            self.template_name,
            {
                "course_formset": course_formset,
            }
        )

    def post(self, request):

        course_formset = CourseFormSet(
            request.POST,
            prefix="courses"
        )

        if not course_formset.is_valid():

            return render(
                request,
                self.template_name,
                {
                    "course_formset": course_formset,
                }
            )

        with transaction.atomic():

            for course_form in course_formset:

                if not course_form.cleaned_data:
                    continue

                if course_form.cleaned_data.get("DELETE"):
                    continue

                course = course_form.save()

                # -----------------------------
                # SUBJECTS
                # -----------------------------

                course_index = course_form.prefix.split("-")[-1]

                subject_formset = SubjectFormSet(
                    request.POST,
                    instance=course,
                    prefix=f"subjects-{course_index}"
                )

                if not subject_formset.is_valid():

                    transaction.set_rollback(True)

                    return render(
                        request,
                        self.template_name,
                        {
                            "course_formset": course_formset,
                            "error": "Please correct the subject details.",
                        }
                    )

                subjects = subject_formset.save()

                # -----------------------------
                # TOPICS
                # -----------------------------

                for subject_index, subject in enumerate(subjects):

                    topic_formset = TopicFormSet(
                        request.POST,
                        instance=subject,
                        prefix=f"topics-{course_index}-{subject_index}"
                    )

                    if not topic_formset.is_valid():

                        transaction.set_rollback(True)

                        return render(
                            request,
                            self.template_name,
                            {
                                "course_formset": course_formset,
                                "error": "Please correct the topic details.",
                            }
                        )

                    topic_formset.save()

        messages.success(
            request,
            "Courses added successfully."
        )

        return redirect("course_list")

class CourseUpdateView(LoginRequiredMixin, View):
    template_name = "students/course_edit.html"

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        course_form = CourseForm(instance=course)

        subject_formset = SubjectFormSet(
            instance=course,
            prefix="subjects"
        )

        subject_rows = []

        for index, subject_form in enumerate(subject_formset.forms):

            topic_formset = TopicFormSet(
                instance=subject_form.instance,
                prefix=f"topics-{index}"
            )

            subject_rows.append({
                "form": subject_form,
                "topic_formset": topic_formset,
            })

        # Used by JavaScript when adding a brand-new subject.
        empty_topic_formset = TopicFormSet(
            prefix="topics-__prefix__"
        )

        return render(
            request,
            self.template_name,
            {
                "form": course_form,
                "subject_formset": subject_formset,
                "subject_rows": subject_rows,
                "empty_topic_formset": empty_topic_formset,
                "course": course,
            }
        )

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        course_form = CourseForm(
            request.POST,
            instance=course
        )

        subject_formset = SubjectFormSet(
            request.POST,
            instance=course,
            prefix="subjects"
        )

        # First validate the course and subject formset.
        course_valid = course_form.is_valid()
        subjects_valid = subject_formset.is_valid()

        print("COURSE VALID:", course_valid)
        print("COURSE ERRORS:", course_form.errors)
        print("SUBJECTS VALID:", subjects_valid)
        print("SUBJECT ERRORS:", subject_formset.errors)
        print(
            "SUBJECT NON-FORM ERRORS:",
            subject_formset.non_form_errors()
        )

        subject_rows = []
        topic_formsets = []
        topics_valid = True

        # Build one TopicFormSet for every subject form using the same index
        # that is used in course_edit.html: topics-0, topics-1, etc.
        if subjects_valid:
            for index, subject_form in enumerate(subject_formset.forms):

                # Ignore completely empty extra subject forms.
                if (
                    not subject_form.instance.pk
                    and not subject_form.has_changed()
                ):
                    continue

                # If this subject is being deleted, its topics will be removed
                # automatically because Topic.subject uses CASCADE.
                if subject_form.cleaned_data.get("DELETE"):
                    continue

                topic_formset = TopicFormSet(
                    request.POST,
                    instance=subject_form.instance,
                    prefix=f"topics-{index}"
                )

                print(
                    f"TOPIC {index} ERRORS:",
                    topic_formset.errors
                )
                print(
                    f"TOPIC {index} NON-FORM ERRORS:",
                    topic_formset.non_form_errors()
                )

                topic_formsets.append(
                    (index, subject_form, topic_formset)
                )

                subject_rows.append({
                    "form": subject_form,
                    "topic_formset": topic_formset,
                })

                if not topic_formset.is_valid():
                    topics_valid = False

        else:
            # Subject validation failed. Rebuild rows so the page can display
            # the submitted subject data and any submitted topic data.
            for index, subject_form in enumerate(subject_formset.forms):

                topic_formset = TopicFormSet(
                    request.POST,
                    instance=subject_form.instance,
                    prefix=f"topics-{index}"
                )

                print(
                    f"TOPIC {index} ERRORS:",
                    topic_formset.errors
                )
                print(
                    f"TOPIC {index} NON-FORM ERRORS:",
                    topic_formset.non_form_errors()
                )

                subject_rows.append({
                    "form": subject_form,
                    "topic_formset": topic_formset,
                })

        if course_valid and subjects_valid and topics_valid:

            with transaction.atomic():

                course = course_form.save()

                # Save/delete subjects one by one so their form index stays
                # matched with the corresponding TopicFormSet.
                for index, subject_form in enumerate(subject_formset.forms):

                    # Completely empty extra subject form.
                    if (
                        not subject_form.instance.pk
                        and not subject_form.has_changed()
                    ):
                        continue

                    # Delete an existing subject.
                    if subject_form.cleaned_data.get("DELETE"):

                        if subject_form.instance.pk:
                            subject_form.instance.delete()

                        continue

                    # Existing or newly added subject.
                    subject = subject_form.save(commit=False)
                    subject.course = course
                    subject.save()

                    if hasattr(subject_form, "save_m2m"):
                        subject_form.save_m2m()

                    # Find the TopicFormSet belonging to this subject index.
                    topic_formset = next(
                        formset
                        for form_index, _, formset in topic_formsets
                        if form_index == index
                    )

                    # For a newly created subject, update the TopicFormSet
                    # instance before saving its topics.
                    topic_formset.instance = subject
                    topic_formset.save()

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect("course_list")

        # Re-render the edit page with validation errors and submitted values.
        empty_topic_formset = TopicFormSet(
            prefix="topics-__prefix__"
        )

        return render(
            request,
            self.template_name,
            {
                "form": course_form,
                "subject_formset": subject_formset,
                "subject_rows": subject_rows,
                "empty_topic_formset": empty_topic_formset,
                "course": course,
                "error": "Please correct the highlighted details.",
            }
        )


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "students/course_confirm_delete.html"
    success_url = reverse_lazy("course_list")


class CertificateTemplateListView(LoginRequiredMixin, ListView):
    model = CertificateTemplate
    template_name = "students/certificate_template_list.html"
    context_object_name = "templates"

    def get_queryset(self):
        return CertificateTemplate.objects.order_by("-created_at")


class CertificateTemplateCreateView(LoginRequiredMixin, CreateView):
    model = CertificateTemplate
    form_class = CertificateTemplateForm
    template_name = "students/certificate_template_form.html"
    success_url = reverse_lazy("certificate_template_list")

class CertificateTemplateUpdateView(LoginRequiredMixin, UpdateView):
    model = CertificateTemplate
    form_class = CertificateTemplateForm
    template_name = "students/certificate_template_form.html"
    success_url = reverse_lazy("certificate_template_list")


class CertificateTemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = CertificateTemplate
    template_name = "students/certificate_template_confirm_delete.html"
    success_url = reverse_lazy("certificate_template_list")

@login_required
def get_student_enrollments(request):
    student_id = request.GET.get("student_id")

    if not student_id:
        return JsonResponse({"enrollments": []})

    enrollments = (
        CourseEnrollment.objects
        .filter(student_id=student_id)
        .select_related("course")
        .order_by("-created_date")
    )

    data = []

    for enrollment in enrollments:
        data.append({
            "id": str(enrollment.course_enrollment_id),
            "course_name": enrollment.course.name,
            "duration_months": enrollment.course.duration_months,
            "status": enrollment.status,
        })

    return JsonResponse({
        "enrollments": data
    })

class CertificateCreateView(LoginRequiredMixin, CreateView):
    model = Certificate
    form_class = CertificateForm
    template_name = "students/certificate_form.html"

    def form_valid(self, form):
        certificate = form.save(commit=False)

        certificate.created_by = self.request.user
        certificate.updated_by = self.request.user

        # First save generates certificate number
        certificate.save()

        enrollment = certificate.course_enrollment
        course = enrollment.course
        template = certificate.template

        # -----------------------------
        # Replace body placeholders
        # -----------------------------

        body_content = template.certificate_body

        replacements = {
            "{{student_name}}": escape(certificate.student.name),
            "{{course_name}}": escape(course.name),
            "{{course_duration}}": str(course.duration_months),
            "{{pass_mark}}": str(certificate.pass_mark),
            "{{certificate_number}}": certificate.certificate_number,
        }

        for placeholder, value in replacements.items():
            body_content = body_content.replace(
                placeholder,
                value
            )

        # -----------------------------
        # Logo
        # -----------------------------

        logo_html = ""

        if template.logo:
            logo_path = template.logo.path

            mime_type, _ = mimetypes.guess_type(logo_path)

            with open(logo_path, "rb") as image_file:
                encoded_image = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            logo_src = (
                f"data:{mime_type};base64,{encoded_image}"
            )

            logo_html = f"""
                <p style="text-align:center;">
                    <img
                        src="{logo_src}"
                        style="
                            max-width:140px;
                            height:auto;
                        "
                    >
                </p>
            """

        # -----------------------------
        # Complete editable certificate
        # -----------------------------

        complete_content = f"""
            {logo_html}

            <h2 style="
                text-align:center;
                margin:5px 0;
                font-size:24px;
            ">
                {escape(template.organization_name)}
            </h2>

            <h1 style="
                text-align:center;
                margin:15px 0 30px 0;
                font-size:34px;
            ">
                {escape(template.certificate_title)}
            </h1>

            <div style="
                font-size:18px;
                line-height:1.7;
                text-align:center;
            ">
                {body_content}
            </div>

            <div style="
                text-align:right;
                margin-top:50px;
            ">
                <p style="
                    margin:0;
                    font-weight:bold;
                ">
                    {escape(template.signature_name)}
                </p>

                <p style="margin:0;">
                    {escape(template.signature_designation)}
                </p>
            </div>

            <div style="
                text-align:center;
                margin-top:40px;
                font-size:12px;
            ">
                {escape(template.footer_text)}
            </div>
        """

        certificate.certificate_content = complete_content
        certificate.save()

        self.object = certificate

        return redirect(
            "certificate_edit_content",
            pk=certificate.pk
        )


class CertificateContentEditView(LoginRequiredMixin, UpdateView):
    model = Certificate
    fields = ["certificate_content"]
    template_name = "students/certificate_content_edit.html"

    def get_success_url(self):
        return reverse_lazy(
            "certificate_preview",
            kwargs={"pk": self.object.pk}
        )

class CertificatePreviewView(LoginRequiredMixin, DetailView):
    model = Certificate
    template_name = "students/certificate_preview.html"
    context_object_name = "certificate"

    
def certificate_pdf_download(request, pk):

    certificate = get_object_or_404(
        Certificate,
        pk=pk
    )

    template = get_template(
        "students/certificate_pdf.html"
    )

    html = template.render({
        "certificate": certificate
    })

    result = BytesIO()

    pdf = pisa.CreatePDF(
        html,
        dest=result,
        encoding="UTF-8",
        link_callback=link_callback
    )

    if pdf.err:

        return HttpResponse(
            "Error generating certificate PDF.",
            status=500
        )

    student_name = (
        certificate.student.name
        .strip()
        .replace(" ", "_")
    )

    year = certificate.issued_date.year

    filename = (
        f"Certificate_{student_name}_{year}.pdf"
    )

    response = HttpResponse(
        result.getvalue(),
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response


def link_callback(uri, rel):

    # Media files
    if uri.startswith(settings.MEDIA_URL):

        path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, "")
        )

        return path

    # Static files
    if uri.startswith(settings.STATIC_URL):

        relative_path = uri.replace(
            settings.STATIC_URL,
            ""
        )

        path = finders.find(relative_path)

        if path:
            return path

    return uri


def certificate_pdf_download(request, pk):
    certificate = get_object_or_404(
        Certificate,
        pk=pk
    )

    html_content = render_to_string(
        "students/certificate_pdf.html",
        {
            "certificate": certificate,
            "base_url": request.build_absolute_uri("/"),
        }
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
            viewport={
                "width": 1120,
                "height": 790
            }
        )

        page.set_content(
            html_content,
            wait_until="networkidle"
        )

        # Use browser/screen styling
        page.emulate_media(media="screen")

        pdf_bytes = page.pdf(
            format="A4",
            landscape=True,
            print_background=True,
            margin={
                "top": "0mm",
                "right": "0mm",
                "bottom": "0mm",
                "left": "0mm",
            },
            prefer_css_page_size=True,
        )

        browser.close()

    student_name = (
        certificate.student.name
        .strip()
        .replace(" ", "_")
    )

    year = certificate.issued_date.year

    filename = (
        f"Certificate_{student_name}_{year}.pdf"
    )

    response = HttpResponse(
        pdf_bytes,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response