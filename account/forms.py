from django import forms
from django.core.exceptions import ValidationError

class UserCreation(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget= forms.TextInput(attrs={
            "id": "username",
            "class": "form-input",
            "placeholder": "Enter an username",
            "tabindex":"1"
    })
    )
    email = forms.EmailField(
        widget= forms.EmailInput(attrs={
            "id": "email", 
            "class": "form-input", 
            "placeholder": "Enter your email",
            "tabindex":"2"
        })
    )
    password1 = forms.CharField(
        min_length=4,
        widget= forms.PasswordInput(attrs={
            "id": "password1",
            "class": "form-input",
            "placeholder": "Enter your password",
            "tabindex":"3"
        })
    )
    password2 = forms.CharField(
        min_length=4,
        widget= forms.PasswordInput(attrs={
            "id": "password2",
            "class": "form-input",
            "placeholder": "Confirm your password",
            "tabindex":"4"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data