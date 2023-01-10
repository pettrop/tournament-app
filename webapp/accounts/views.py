from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render


class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('signupsuccessful')  #TO BE changed to real main page after it's development

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        username = cleaned_data['username']
        password = cleaned_data['password1']
        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            login(self.request, new_user)
        return result

#Below for TEST purposes only!


def signupsuccessful(request):
    return HttpResponse("Signup was successfull!")


def loginsuccessful(request):
    template = "home.html"
    context = {}
    return render(request, template, context)
