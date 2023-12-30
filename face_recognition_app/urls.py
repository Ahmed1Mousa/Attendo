# face_recognition_app/urls.py
from django.urls import path
from .views import upload_image

app_name = "face_recognition_app"


urlpatterns = [
    path("upload_image/", upload_image, name="upload_image"),
]
