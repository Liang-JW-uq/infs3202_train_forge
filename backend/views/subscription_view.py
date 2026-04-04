from django.shortcuts import render, redirect

def subscription_list(request):
    return render(request, "backend/subscription_list.html")

def subscription_add(request):
    return render(request, "backend/subscription_add.html")

def subscription_edit(request):
    return render(request, "backend/subscription_edit.html")

def subscription_delete(request):
    return render(request, "backend/subscription_delete.html")

