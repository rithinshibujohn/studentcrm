from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Student
from .forms import StudentForm


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


class StudentDetailView(LoginRequiredMixin,
                        DetailView):

    model = Student
    template_name = "students/student_detail.html"