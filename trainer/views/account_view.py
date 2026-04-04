from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

UserTrainer = get_user_model()

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')

        # for simplicity, will consider username = email
        # and for social login
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # If Trainer, we redirect to Trainer Application
            # If Admin, we redirect to the SaaS Admin page
            if user.is_trainer:             # Saas tenant redirect
                return redirect('home') 
            elif user.is_staff:
                return redirect('subscription_list')

            return redirect('index')        
        else:
            messages.error(request, "Invalid Email or Password")
            return redirect('login')

    return render(request, 'registration/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if UserTrainer.objects.filter(username=email).exists():
            messages.error(request, "Email already taken!")
            return redirect('register')

        # will set username = email
        new_userTrainer = UserTrainer.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_trainer=True     # rmb to set this as a trainer
        )

        # attach to existing 'Free' group all new trainer
        # RMB: *** the groups has to be manually created first after first migration
        try:
            free_group = Group.objects.get(name='Free')     #default group
            new_userTrainer.groups.add(free_group)

            messages.success(request, "Account created successfully!")
        except Exception as e:
            messages.error(request, str(e))
        # except Group.DoesNotExist:
        #     print("WARNING: 'Free' group not found in DB. User created without group.")

        return redirect('login')

    return render(request, 'registration/register.html')

