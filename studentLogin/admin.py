from django.contrib import admin

# Register your models here.

# filepath: c:\Users\sathv\project\core\studentLogin\admin.py
from django.contrib import admin
from .models import *

@admin.register(studentReg)
class StudentRegAdmin(admin.ModelAdmin):
    list_display = ('studentName', 'hallTicketNum', 'phoneNum' , 'image' , 'studentPassword')  # Customize fields to display

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('qr_code_data', 'faculty', 'created_at')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'marked_at')
    list_filter = ('session',)

