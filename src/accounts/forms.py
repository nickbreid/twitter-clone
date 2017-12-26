from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords must match.")
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__icontains=username).exists():
            raise forms.ValidationError("Username is taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError("Email is taken.")
        return email
