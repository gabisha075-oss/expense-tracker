from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import UserProfile

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required')
            return render(request, 'register.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('landing')

@login_required(login_url='login')
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.bio = request.POST.get('bio')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    
    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
@require_POST
def change_password(request):
    old_password = request.POST.get('old_password')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')
    
    if not request.user.check_password(old_password):
        return JsonResponse({'success': False, 'message': 'Current password is incorrect'})
    
    if new_password1 != new_password2:
        return JsonResponse({'success': False, 'message': 'New passwords do not match'})
    
    if len(new_password1) < 8:
        return JsonResponse({'success': False, 'message': 'Password must be at least 8 characters'})
    
    request.user.set_password(new_password1)
    request.user.save()
    
    return JsonResponse({'success': True, 'message': 'Password changed successfully'})
