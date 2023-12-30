from django.shortcuts import render
from .models import Student, Attendance
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AttendanceForm


def student_list(request):
    date_filter = request.GET.get("date_filter")
    students = Student.objects.all()

    if date_filter:
        attendance_records = Attendance.objects.filter(date=date_filter).values(
            "student_id", "present"
        )
        attendance_dict = {
            record["student_id"]: record["present"] for record in attendance_records
        }

        for student in students:
            student.attended = attendance_dict.get(student.id, False)

    return render(
        request,
        "attendance/index.html",
        {"students": students, "date_filter": date_filter},
    )


def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, "student_detail.html", {"student": student})


def mark_attendance(request):
    if request.method == "POST":
        # Get the list of selected student IDs
        students = Student.objects.all()
        attendance_date = request.POST.get("attendance_date")

        # Save attendance records to the database for each selected student
        for student in students:
            present = request.POST.get(f"present_{student.id}", False)
            if present == "on":
                present = False
            else:
                present = True
            attendance = Attendance(
                student_id=student.id, date=attendance_date, present=present
            )
            attendance.save()

    # Redirect to a suitable page after marking attendance
    return redirect("student_list")


def reset_attendance(request, date_filter):
    # Set attendance records for the specified date to False
    Attendance.objects.filter(date=date_filter).update(present=False)
    return redirect("student_list")


def edit_attendance(request, date_filter):
    # Get all students
    students = Student.objects.all()
    if date_filter:
        attendance_records = Attendance.objects.filter(date=date_filter).values(
            "student_id", "present"
        )
        attendance_dict = {
            record["student_id"]: record["present"] for record in attendance_records
        }

        for student in students:
            student.attended = attendance_dict.get(student.id, False)

    if request.method == "POST":
        # Update or create attendance records based on the form data
        for student in students:
            attendance, created = Attendance.objects.get_or_create(
                student_id=student.id, date=date_filter
            )
            print(student.id)
            if request.POST.get(f"present_{student.id}"):
                present = request.POST.get(f"present_{student.id}")
                if present == "on":
                    present = False
                else:
                    present = True
                print(present)
                attendance.present = present
            else:
                attendance.present = True
            attendance.save()

        return redirect("student_list")
    return render(
        request,
        "attendance/edit_attendance.html",
        {"students": students, "date_filter": date_filter},
    )


def upload_image(request):
    return render(request, "attendance/upload_image.html")


def add_attendance(request):
    students = Student.objects.all()
    return render(request, "attendance/add_attendance.html", {"students": students})
