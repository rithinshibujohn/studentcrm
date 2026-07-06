from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import Student


# Create your views here.
@login_required
def dashboard(request):
    context = {
        "student_count": Student.objects.count(),
        "user_count": User.objects.count(),
        "recent_students": Student.objects.order_by("-created_at")[:5],
    }
    return render(request, "dashboard.html", context)


from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)

from .forms import UserForm

class UserListView(LoginRequiredMixin,ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    ordering = ["username"]


class UserCreateView(LoginRequiredMixin,CreateView):
    model = User
    form_class = UserForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "User created successfully.")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("user_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["password"].required = False
        return form

    def form_valid(self, form):
        messages.success(self.request, "User updated successfully.")
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "user_obj"

@login_required
def profile(request):
    return redirect("user_edit", pk=request.user.id)