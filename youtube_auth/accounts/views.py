
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile
from django.contrib.auth.models import User


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = UserProfile.objects.create(user=user)
            return redirect(f'/verify/{profile.token}/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def verify_view(request, token):
    try:
        profile = UserProfile.objects.get(token=token)
        profile.is_verified = True
        profile.user.is_active = True
        profile.user.save()
        profile.save()
        
        return render(request,'verify.html')
    except:
        return render(request, 'verify.html', {'error': 'Invalid token'})


  
   
  
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, 'userprofile') and user.userprofile.is_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Account not verified.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')
