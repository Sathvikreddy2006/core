from django.db import models
from faculty.models import facultyReg

# Create your models here.

class studentReg(models.Model):
    
    studentName = models.CharField(max_length=30 )
    hallTicketNum = models.CharField(max_length=20, unique=True)
    phoneNum = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to='studentImages/' )
    studentPassword = models.CharField(max_length=20)

    def __str__(self):
        return self.studentName

class AttendanceSession(models.Model):
    qr_code_data = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(facultyReg, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.faculty.facultyName} - {self.created_at}"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(studentReg, on_delete=models.CASCADE)
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'session')

    def __str__(self):
        return f"{self.student.studentName} - {self.session}"
    


