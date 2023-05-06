from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            context = {
                "form": form,
            }
            return render(request, 'accounts/register.html', context)
        return redirect(reverse('login'))
    if request.method == "GET":
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect(reverse('home'))

            return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse("login"))