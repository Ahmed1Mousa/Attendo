from django.urls import path
from attendance.views import (
    student_list,
    mark_attendance,
    reset_attendance,
    add_attendance,
    edit_attendance,
    export_attendance,
)

urlpatterns = [
    path("", student_list, name="student_list"),
    path("mark_attendance/", mark_attendance, name="mark_attendance"),
    path(
        "reset_attendance/<str:date_filter>/", reset_attendance, name="reset_attendance"
    ),
    path(
        "edit_attendance/<str:date_filter>/",
        edit_attendance,
        name="edit_attendance",
    ),
    path("add_attendance/", add_attendance, name="add_attendance"),
    path("export_attendance/", export_attendance, name="export_attendance"),
]
