from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import Student
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.views.generic import UpdateView


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

from .forms import UserEditForm, UserForm, ProfileForm

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
    form_class = UserEditForm
    template_name = "accounts/user_edit.html"
    success_url = reverse_lazy("user_list")

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


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("change_password")

    def form_valid(self, form):
        response = super().form_valid(form)

        update_session_auth_hash(self.request, form.user)

        messages.success(
            self.request,
            "Password changed successfully."
        )

        return response
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)
    
    

