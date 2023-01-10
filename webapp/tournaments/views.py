from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.
def main_view(request):
    return HttpResponse('Tournament APP!')


# KUBO
def home(request):
    template = "home.html"
    context = {}
    return render(request, template, context)

def results(request):
    template = "results.html"
    context = {}
    return render(request, template, context)

