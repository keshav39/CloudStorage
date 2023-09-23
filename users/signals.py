# signals.py
from .models import UploadedFile, CustomUser
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from .models import UploadedFile, CustomUser  # Import your UploadedFile model


@receiver(pre_delete, sender=CustomUser)
def delete_user_files(sender, instance, **kwargs):
    # Get all files associated with the user and delete them
    user_files = UploadedFile.objects.filter(user=instance)
    for file in user_files:
        file.file.delete()  # Delete the actual file from storage
        file.delete()  # Delete the file record from the database


# signals.py


@receiver(pre_delete, sender=User)
def delete_user_files(sender, instance, **kwargs):
    # Check if the user is attempting to delete themselves
    current_user = instance  # Assuming you have the current user
    if current_user == instance:
        return  # Prevent deletion if user tries to delete themselves

    # Get all files associated with the user and delete them
    user_files = UploadedFile.objects.filter(user=instance)
    for file in user_files:
        file.file.delete()  # Delete the actual file from storage
        file.delete()  # Delete the file record from the database


@receiver(post_delete, sender=UploadedFile)
def decrease_file_counter(sender, instance, **kwargs):
    # Decrement the file counter attribute in the CustomUser model
    user = instance.user
    if user.file_counter > 0:
        user.file_counter -= 1
        user.save()
