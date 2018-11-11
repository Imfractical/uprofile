import datetime

from django import forms
from django.contrib.auth import password_validation

from .models import User


class UserCreationForm(forms.ModelForm):
    email1 = forms.EmailField(
        label='Email',
        help_text='Enter your email',
    )
    email2 = forms.EmailField(
        label='Email confirmation',
        help_text='Enter the same email as before, for verification',
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_texts(),
    )
    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification',
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'dob']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "The two password don't match",
                code='password_mismatch',
            )

        return password2

    def clean_email2(self):
        email1 = self.cleaned_data.get('email1')
        email2 = self.cleaned_data.get('email2')
        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                "The two emails don't match",
                code='email_mismatch',
            )

        return email2

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if datetime.datetime.now - dob < 13:
            raise forms.ValidationError(
                "You're too young!",
                code='underage',
            )

        return dob

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data by super()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email1']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user
