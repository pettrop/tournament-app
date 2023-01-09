from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect


def register(request):
    if request.user.is_authenticated:
        return redirect('fakemain') #má vrátit na hlavní stránku až bude

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('signupsuccessful')

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

# class SignUpView(CreateView):
#     template_name = 'accounts/signup.html'
#     form_class = UserCreationForm
#     success_url = reverse_lazy('signupsuccessful')  #TO BE changed to real main page after it's development
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         cleaned_data = form.cleaned_data
#         username = cleaned_data['username']
#         password = cleaned_data['password1']
#         new_user = authenticate(username=username, password=password)
#         if new_user is not None:
#             login(self.request, new_user)
#         return result

#Below for TEST purposes only!


def signupsuccessful(request):
    return HttpResponse("Signup was successfull!")


def loginsuccessful(request):
    return HttpResponse("Login was successful!")


def mainpage(request):
    return HttpResponse("Main page!")
