from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.forms import UserLoginForm


# Create your views here.


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        print('1')
        email = data.get('email')
        print(email)
        password = data.get('password')
        print(password)
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')
