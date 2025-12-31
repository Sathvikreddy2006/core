from django.shortcuts import render

from django.http import HttpResponse

def home1 (request):
    return render(request , "preface.html")


