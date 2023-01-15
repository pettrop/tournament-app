from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.views.generic import DetailView

from .models import User, Profile
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
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


@login_required
def profile(request):
    user = request.user
    profile = request.user.profile
    context = {'user': user, 'profile': profile}
    return render(
        request=request,
        template_name='accounts/profile.html',
        context=context
    )


@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

        else:
            for error in list(user_form.errors.values()):
                print(request, error)

            for error in list(profile_form.errors.values()):
                print(request, error)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request=request, template_name='accounts/profile_update.html', context=context)
