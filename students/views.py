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

from .models import Student, Course, Subject
from .forms import (
    StudentForm,
    EducationDetailFormSet,
    CourseEnrollmentFormSet,
    StudentForm,
    CourseForm,
    SubjectForm,    
    SubjectFormSet,
    CourseFormSet
)
from django.db import transaction
from .utils import import_students_from_excel
from .excel_form import ExcelUploadForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .pdf import generate_student_pdf
from django.db import transaction
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
)


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

                # Subjects for this course
                subject_formset = SubjectFormSet(
                    request.POST,
                    instance=course,
                    prefix=f"subjects-{course_form.prefix.split('-')[-1]}"
                )

                if subject_formset.is_valid():
                    subject_formset.save()
                else:
                    transaction.set_rollback(True)

                    return render(
                        request,
                        self.template_name,
                        {
                            "course_formset": course_formset,
                            "error": "Please correct the subject details.",
                        }
                    )

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

        return render(
            request,
            self.template_name,
            {
                "form": course_form,
                "subject_formset": subject_formset,
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

        if course_form.is_valid() and subject_formset.is_valid():

            with transaction.atomic():

                course_form.save()
                subject_formset.save()

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect("course_list")

        return render(
            request,
            self.template_name,
            {
                "form": course_form,
                "subject_formset": subject_formset,
                "course": course,
            }
        )


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "students/course_confirm_delete.html"
    success_url = reverse_lazy("course_list")