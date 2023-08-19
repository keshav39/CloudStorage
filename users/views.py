import os
from .forms import FileUploadForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *


def landing(request):
    return render(request, 'home.html')


# def content_file_name(instance, file):
#     ext = file.file.split('.')[-1]
#     filename = "%s_%s.%s" % (instance.user.id, instance.file.id, ext)
#     return ('uploads' / filename)


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
    return render(request, 'upload.html', {'form': form})


def delete_file(self, request, file_id):
    user = request.session['user']
    delete_file = self.model.objects.get(id=file_id)
    delete_file.delete()
    messages.success(request, 'Your post has been deleted successfully.')
    return redirect('profile')


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
