import os
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *


def landing(request):
    return render(request, 'home.html')


def upload_file(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            # Redirect to the user's profile or any other appropriate page
            return redirect('profile')
    else:
        form = FileUploadForm()

    context = {
        'form': form,
    }
    return render(request, 'upload.html', context)


def delete_file(request, file_id):
    if not request.user.is_authenticated:
        return redirect('login')
    file_to_delete = get_object_or_404(
        UploadedFile, id=file_id, user=request.user)
    if request.method == 'POST':
        file_to_delete.file.delete()
        file_to_delete.delete()

        return redirect('profile')

    context = {
        'file_to_delete': file_to_delete,
    }
    return render(request, 'delete.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def profile(request):
    if (request.user.is_authenticated):
        user = request.user
        uploaded_files = UploadedFile.objects.filter(user=user)
        context = {
            'user': user,
            'uploaded_files': uploaded_files,
        }
        return render(request, 'profile.html', context)
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Logged in as {user.username}')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    return redirect('login')
