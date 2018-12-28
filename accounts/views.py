from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
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


@user_passes_test(lambda u: u.is_anonymous)
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)

                    return redirect('accounts:profile', args=[user.id])
                else:
                    messages.error(
                        request,
                        "This account is inactive",
                    )
        else:
            messages.error(
                request,
                "Please enter a correct email and password",
            )
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


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
    user = request.user
    form = PasswordChangeForm(user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed successfully")

            return redirect('accounts:view_profile')

    return render(request, 'accounts/change_password.html', {
            'form': form,
            'user': user,
    })
