from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import ProfileForm, UserForm


def home(request):
    return render(request, 'accounts/home.html')


@user_passes_test(lambda u: u.is_anonymous)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "User registration successful! Welcome, {}".format(user.first_name)
            )

            return redirect('accounts:view_profile')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def signout(request):
    logout(request)

    return redirect('accounts:home')


@login_required
def view_profile(request, user_pk=None):
    if not user_pk:
        user = request.user
    else:
        user = User.objects.get(pk=user_pk)
    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=user.profile)

    return render(request, 'accounts/view_profile.html', {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
@transaction.atomic
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Successfully updated profile")

            return redirect('accounts:view_profile')
        else:
            messages.error(request, "Couldn't update profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Successfully updated password")

            return redirect('accounts:view_profile')
        else:
            messages.error(request, "Password could not be updated")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
