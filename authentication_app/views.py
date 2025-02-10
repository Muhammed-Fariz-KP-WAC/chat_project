from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile
from django.views import View
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not all([username, password, email]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user)
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validations
        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('rooms')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')