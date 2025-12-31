from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import facultyReg


@admin.register(facultyReg)
class FacultyRegAdmin(admin.ModelAdmin):
    list_display = ('facultyName', 'facultyId', 'phoneNum' , 'image' , 'facultyPassword')  # Customize fields to display