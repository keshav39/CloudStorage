import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings


def rename_file(instance, filename):
    # Get the file's extension
    ext = filename.split('.')[-1]
    instance.user.file_counter += 1
    instance.user.save()
    new_filename = f"{instance.user.username}_{instance.user.file_counter}.{ext}"

    return os.path.join('uploads', new_filename)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None):
        user = self.create_user(email, username, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    file_counter = models.PositiveIntegerField(default=0)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.username


class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to=rename_file)
    file_name = models.CharField(max_length=255)
    description = models.CharField(blank=True, max_length=255)

    shared_with = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='shared_files', blank=True)

    def __str__(self):
        return self.file_name
