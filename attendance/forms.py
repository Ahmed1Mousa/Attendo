# attendance_system/forms.py

from django import forms
from .models import Student


class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)

        # Dynamically add a BooleanField for each student
        students = Student.objects.all()
        for student in students:
            self.fields[str(student.id)] = forms.BooleanField(
                label=student.name, required=False
            )


class ExportAttendanceForm(forms.Form):
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.IntegerField(min_value=2000, max_value=2100)
