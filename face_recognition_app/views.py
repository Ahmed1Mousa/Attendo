# views.py
import os
from datetime import date
from django.http import HttpResponse
from .forms import ImageUploadForm
from .cv_codes.predict import recognize_faces
from django.shortcuts import render
from attendance.models import Student


def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data["image"]

            # Create a folder based on the current date
            today_folder = date.today().strftime("%Y-%m-%d")
            media_folder = "media"
            upload_folder_path = os.path.join(media_folder, today_folder)

            # Ensure the folder exists
            os.makedirs(upload_folder_path, exist_ok=True)

            # Save the uploaded image to the folder
            uploaded_image_path = os.path.join(upload_folder_path, uploaded_image.name)
            with open(uploaded_image_path, "wb") as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            # Call your face recognition script with the image path
            output, output_image_path = recognize_faces(uploaded_image_path)
            students_ids = []
            for i in output:
                students_ids.append(int(i))
            all_students = Student.objects.all()
            print(students_ids)
            return render(
                request,
                "computer_vision/face_recognition_result.html",
                {
                    "original_image_path": uploaded_image_path,
                    "output_image_path": output_image_path,
                    "output": output,
                    "students_ids": students_ids,
                    "all_students": all_students,
                },
            )
    else:
        form = ImageUploadForm()

    return render(request, "computer_vision/upload_image.html", {"form": form})
