from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path("", views.dashboard, name="dashboard"),

    # Authentication
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # Profile
    path("profile/", views.profile, name="profile"),

    # User Management
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/add/", views.UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("change-password/",
    auth_views.PasswordChangeView.as_view(
        template_name="registration/change_password.html",
        success_url=reverse_lazy("dashboard"),
    ),
    name="change_password",
),
]