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
from .forms import StudentForm
from .utils import import_students_from_excel
from .excel_form import ExcelUploadForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .pdf import generate_student_pdf
from django.conf import settings
import os

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"


class StudentCreateView(LoginRequiredMixin,
                        SuccessMessageMixin,
                        CreateView):

    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"

    success_url = reverse_lazy("student_list")

    success_message = "Student added successfully."


class StudentUpdateView(LoginRequiredMixin,
                        SuccessMessageMixin,
                        UpdateView):

    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"

    success_url = reverse_lazy("student_list")

    success_message = "Student updated successfully."


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


def media_test(request):
    media_root = settings.MEDIA_ROOT
    files = []

    if os.path.exists(media_root):
        for root, dirs, filenames in os.walk(media_root):
            for f in filenames:
                files.append(os.path.join(root, f))

    return HttpResponse("<br>".join(files) if files else "No files found")