from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from decouple import config
from .models import CustomUser


def landing(request):
    return render(request, "home.html")


def upload_file(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            # Redirect to the user's profile or any other appropriate page
            return redirect("profile")
    else:
        form = FileUploadForm()

    context = {
        "form": form,
    }
    return render(request, "upload.html", context)


def delete_file(request, file_id):
    if not request.user.is_authenticated:
        return redirect("login")
    file_to_delete = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    if request.method == "POST":
        file_to_delete.file.delete()
        file_to_delete.delete()

    context = {
        "file_to_delete": file_to_delete,
    }
    return render(request, "delete_file.html", context)


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            master_key = form.cleaned_data.get("master_key")
            if master_key == config("KEY"):
                user.is_staff = True
            user.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        uploaded_files = UploadedFile.objects.filter(user=user)
        shared_files = UploadedFile.objects.filter(shared_with=user)
        context = {
            "user": user,
            "uploaded_files": uploaded_files,
            "shared_files": shared_files,
        }
        return render(request, "profile.html", context)
    return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in as {user.username}")
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    return redirect("login")


def share(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    uploaded_files = UploadedFile.objects.filter(user=user)

    if request.method == "POST":
        form = ShareFilesForm(user, request.POST)
        if form.is_valid():
            selected_files = form.cleaned_data.get("selected_files")
            recipients = form.cleaned_data.get("recipients")

            # Validate selected_files to ensure they belong to the user
            valid_selected_files = UploadedFile.objects.filter(
                id__in=selected_files, user=user
            )

            if len(valid_selected_files) != len(selected_files):
                # Some selected files don't belong to the user, handle the error
                return render(
                    request,
                    "share.html",
                    {"form": form, "error_message": "Invalid file selection."},
                )

            for file_to_share in valid_selected_files:
                # Share the file with selected recipients
                file_to_share.shared_with.add(*recipients)

            return redirect("profile")
    else:
        form = ShareFilesForm(user=user)

    context = {
        "form": form,
        "uploaded_files": uploaded_files,
    }
    return render(request, "share.html", context)


def manage_files(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        # Redirect to a page with an access denied message for non-admin users
        return render(request, "denied.html")

    if request.method == "POST":
        file_id = request.POST.get("file_id")
        file_to_delete = get_object_or_404(UploadedFile, id=file_id)
        file_to_delete.file.delete()
        file_to_delete.delete()

    # Get all uploaded files
    users = CustomUser.objects.all()
    uploaded_files = UploadedFile.objects.all()

    context = {
        "users": users,
        "uploaded_files": uploaded_files,
    }

    return render(request, "file_admin.html", context)


def manage_users(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        # Redirect to an access denied page for non-admin users
        return render(request, "denied.html")

    # Get all users
    users = CustomUser.objects.all()

    context = {
        "users": users,
    }

    return render(request, "user_admin.html", context)


def manage(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        # Redirect to an access denied page for non-admin users
        return render(request, "denied.html")

    return render(request, "manage.html")


def delete_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        # Redirect to an access denied page for non-admin users
        return render(request, "denied.html")

    if request.method == "POST":
        # Delete the user with the specified user_id
        user_to_delete = CustomUser.objects.get(pk=user_id)
        user_to_delete.delete()

    return redirect("manage_users")


def promote_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.is_staff:
        # Redirect to an access denied page for non-admin users
        return render(request, "denied.html")

    if request.method == "POST":
        # Promote the user with the specified user_id to admin
        user_to_promote = CustomUser.objects.get(pk=user_id)
        user_to_promote.is_staff = True
        user_to_promote.save()
    return redirect("manage_users")


def confirm_delete(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        # If the user confirms deletion, delete the user and related files
        user = request.user
        user.delete()
        # Redirect to the logout view or any other appropriate view
        return redirect("logout")

    context = {
        "users": request.user,
    }

    return render(request, "confirm_delete.html", context)


def file_search(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "GET":
        form = FileSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # Search for files based on the query
            uploaded_files = UploadedFile.objects.filter(
                Q(file_name__icontains=query) | Q(description__icontains=query),
                user=request.user,
            )

            # Search in shared files
            shared_files = UploadedFile.objects.filter(
                Q(file_name__icontains=query) | Q(description__icontains=query),
                shared_with=request.user,
            )

            context = {
                "uploaded_files": uploaded_files,
                "shared_files": shared_files,
                "query": query,
                "form": form,
            }
            return render(request, "search.html", context)
    else:
        form = FileSearchForm()

    return render(request, "search.html", {"form": form})
