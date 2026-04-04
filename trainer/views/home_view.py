from django.shortcuts import render, redirect

def home(request):
    return render(request, "trainer/home.html", {})