from django.shortcuts import render, redirect

def index(request):
    return render(request, "trainer/index.html", {'layout': 'public'})