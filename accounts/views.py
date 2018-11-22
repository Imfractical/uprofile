from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .forms import UserCreationForm


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email1')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('accounts:signup')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})
