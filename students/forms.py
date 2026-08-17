from django import forms
from django.forms import inlineformset_factory

from .models import (
    Student,
    EducationDetail,
    CourseEnrollment,
)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "name",
            "email",
            "phone",
            "dob",
            "gender",
            "address",
            "course",
            "photo",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "dob": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "gender": forms.Select(
                attrs={"class": "form-control"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),
            "course": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "photo": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }


class EducationDetailForm(forms.ModelForm):
    class Meta:
        model = EducationDetail
        fields = [
            "qualification",
            "institution",
            "year",
            "percentage",
        ]

        widgets = {
            "qualification": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "institution": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1900",
                    "max": "2100",
                }
            ),
            "percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                }
            ),
        }


class CourseEnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = [
            "course",
            "start_date",
            "fee",
            "status",
        ]

        widgets = {
            "course": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "status": forms.Select(
                attrs={"class": "form-control"}
            ),
        }


EducationDetailFormSet = inlineformset_factory(
    Student,
    EducationDetail,
    form=EducationDetailForm,
    extra=1,
    can_delete=True,
)


CourseEnrollmentFormSet = inlineformset_factory(
    Student,
    CourseEnrollment,
    form=CourseEnrollmentForm,
    extra=1,
    can_delete=True,
)