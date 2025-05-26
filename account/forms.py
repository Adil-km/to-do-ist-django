from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Form for Signup
class SignupForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=150, 
        widget= forms.TextInput(attrs={
            "id": "username",
            "class": "form-input",
            "placeholder": "Enter a username",
            "tabindex":"1",
            "minlength":"4"
        })
    )
    email = forms.EmailField(
        widget= forms.EmailInput(attrs={
            "id": "email", 
            "class": "form-input", 
            "placeholder": "Enter your email",
            "tabindex":"2",
            "minlength":"4"
        })
    )
    password1 = forms.CharField(
        min_length=4,
        widget= forms.PasswordInput(attrs={
            "id": "password1",
            "class": "form-input",
            "placeholder": "Enter a password",
            "tabindex":"3",
            "minlength":"4"
        })
    )
    password2 = forms.CharField(
        min_length=4,
        widget= forms.PasswordInput(attrs={
            "id": "password2",
            "class": "form-input",
            "placeholder": "Confirm your password",
            "tabindex":"4",
            "minlength":"4"
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
    
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user

# Form for Login
class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=150, 
        widget= forms.TextInput(attrs={
            "id": "username",
            "class": "form-input",
            "placeholder": "Enter your username",
            "tabindex":"1",
        })
    )
    password = forms.CharField(
        min_length=4,
        widget= forms.PasswordInput(attrs={
            "id": "password",
            "class": "form-input",
            "placeholder": "Enter your password",
            "tabindex":"2",
        })
    )