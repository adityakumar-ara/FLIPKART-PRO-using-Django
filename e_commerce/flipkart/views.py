import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render

from .models import CustomUser


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not full_name or not email or not password:
            messages.error(request, 'Please fill all fields.')
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        username = email.split('@')[0]

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'register.html')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            mobile_no=f'u{uuid.uuid4().hex[:14]}',
        )
        auth_login(request, user)
        messages.success(request, 'Registration successful.')
        return redirect('/')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Please fill all fields.')
            return render(request, 'login.html')

        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user_obj = None

        user = authenticate(
            request,
            username=user_obj.username if user_obj else email,
            password=password,
        )

        if user is None:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

        auth_login(request, user)
        messages.success(request, 'Login successful.')
        return redirect('/')

    return render(request, 'login.html')
