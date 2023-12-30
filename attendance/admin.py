from django.contrib import admin
from .models import Student, Attendance


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "uniId",
        "name",
    ]


class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "student",
        "present",
    ]


admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
