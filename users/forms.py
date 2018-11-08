from django import forms


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    email_confirmation = forms.EmailField()
    password = forms.CharField(min_length=14, max_length=100, widget=forms.PasswordInput)
    password_confirmation = forms.CharField()
    dob = forms.DateField()
