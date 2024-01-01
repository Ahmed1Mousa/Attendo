from django.shortcuts import render
from .models import Student, Attendance
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AttendanceForm, ExportAttendanceForm
from datetime import date, datetime, timedelta
import csv
from calendar import monthrange
from io import StringIO
from django.http import HttpResponse


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
        if not attendance_date:
            attendance_date = date.today()

        # Save or update attendance records for each selected student
        for student in students:
            present = request.POST.get(f"present_{student.id}")

            # Check if an attendance record already exists for the student on the given date
            existing_record = Attendance.objects.filter(
                student_id=student.id, date=attendance_date
            ).first()

            if present == "on":
                present = False
            else:
                present = True

            # If an attendance record exists, update it; otherwise, create a new one
            if existing_record:
                existing_record.present = present
                existing_record.save()
            else:
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


def add_attendance(request):
    students = Student.objects.all()
    return render(request, "attendance/add_attendance.html", {"students": students})


def export_attendance(request):
    if request.method == "POST":
        month = request.POST.get("month")
        year = request.POST.get("year")

        # Get the first and last day of the selected month
        first_day = datetime(int(year), int(month), 1)
        last_day = datetime(int(year), int(month), monthrange(int(year), int(month))[1])

        # Get all students and attendance records for the selected month
        students = Student.objects.all()
        attendance_records = Attendance.objects.filter(
            date__range=[first_day, last_day]
        )

        # Create a CSV file in memory
        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)

        # Write the header row with UniID, name, and email
        header_row = ["UniID", "Name", "Email"]
        current_day = first_day
        while current_day <= last_day:
            header_row.append(current_day.strftime("%Y-%m-%d"))
            current_day += timedelta(days=1)
        csv_writer.writerow(header_row)

        # Write attendance data for each student
        for student in students:
            row_data = [student.uniId, student.name, student.email]
            current_day = first_day
            while current_day <= last_day:
                attendance = attendance_records.filter(
                    student=student, date=current_day
                ).first()
                if attendance:
                    row_data.append("Present" if attendance.present else "Absent")
                else:
                    row_data.append("Absent")
                current_day += timedelta(days=1)
            csv_writer.writerow(row_data)

        # Create the HTTP response with CSV file
        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="attendance_{month}_{year}.csv"'
        response.write(csv_file.getvalue())
        return response
    else:
        form = ExportAttendanceForm()
        return render(
            request, "attendance/export_attendance.html", {"export_form": form}
        )
