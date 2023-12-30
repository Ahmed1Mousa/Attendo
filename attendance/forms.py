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
