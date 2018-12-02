from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import UserCreationForm
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
    pass
