from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Student
from .forms import (
    StudentForm,
    EducationDetailFormSet,
    CourseEnrollmentFormSet,
)
from django.db import transaction
from .utils import import_students_from_excel
from .excel_form import ExcelUploadForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .pdf import generate_student_pdf


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


