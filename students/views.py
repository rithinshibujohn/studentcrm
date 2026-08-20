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

from .models import Student, Course, Subject,Topic
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
