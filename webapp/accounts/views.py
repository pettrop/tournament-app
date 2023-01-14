from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="accounts/signup.html",
        context={"form": form}
    )


@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                return redirect('home')

        else:
            for error in list(form.errors.values()):
                print(request, error)

    else:
        form = AuthenticationForm()

    return render(
        request=request,
        template_name="registration/login.html",
        context={"form": form}
    )