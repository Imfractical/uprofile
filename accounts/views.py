from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import AuthenticationForm, UserCreationForm
from .models import User


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email1']
            password = form.cleaned_data['password1']
            login(request, authenticate(email=email, password=password))
            user = User.objects.get(email=email)
            messages.success(
                request,
                "User registration successful! Welcome, {}".format(user.first_name)
            )

            return redirect('accounts:profile', args=[user.id])
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


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

    return render(request, 'accounts/signin.html', {'form': form})


def signout(request):
    logout(request)
    messages.success(request, "Logout successful. Goodbye")

    return redirect('home')
