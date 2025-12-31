from django import forms
from .models import studentReg
from django.contrib.auth.forms import AuthenticationForm


class StudentRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = studentReg
        fields = ['studentName', 'hallTicketNum', 'phoneNum', 'image', 'studentPassword']
        widgets = {
            
            'studentName': forms.TextInput(attrs={'class': 'form-control'}),
            'hallTicketNum': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'studentPassword': forms.PasswordInput(attrs={'class': 'form-control'}),
            'phoneNum': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("studentPassword")
        confirm_password = cleaned_data.get("confirm_password")
        print("🛠 Clean method called")
        print(f"Password: {password}, Confirm: {confirm_password}")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")


class StudentLoginForm(forms.Form):
    hallTicketNum = forms.CharField(label="hallTicketNum", max_length=150)
    studentPassword = forms.CharField(label="studentPassword", widget=forms.PasswordInput)