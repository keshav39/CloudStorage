from .models import *
from django import forms
from decouple import config
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    master_key = forms.CharField(max_length=100, required=False, widget=forms.PasswordInput(
        attrs={'master_key': config('KEY')}))

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_number',
                  'password1', 'password2', 'master_key')


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'file_name', 'description']


class ShareFilesForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ShareFilesForm, self).__init__(*args, **kwargs)

        # Dynamically populate choices for selected_files based on the user's uploaded files
        self.fields['selected_files'].queryset = UploadedFile.objects.filter(
            user=user)

    selected_files = forms.ModelMultipleChoiceField(
        queryset=UploadedFile.objects.none(),  # Initialize as an empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=True,  # This field is not required
    )

    recipients = forms.ModelMultipleChoiceField(
        # You can adjust this queryset based on your needs
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,  # This field is not required
    )
