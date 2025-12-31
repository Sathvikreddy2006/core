from django.db import models

# Create your models here.
class facultyReg(models.Model):
    facultyName = models.CharField(max_length=30)
    facultyId = models.CharField(max_length=20, unique=True, default="null")
    phoneNum = models.CharField(max_length=15, unique=True, default="null")
    image = models.ImageField(upload_to='facultyImages/', default='facultyImages/default.png')
    facultyPassword = models.CharField(max_length=10, default="null")

    def __str__(self):
        return self.facultyName
    