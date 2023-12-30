from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    uniId = models.IntegerField()
    email = models.EmailField(max_length=254)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
