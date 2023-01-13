from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView
from django.template import defaulttags
from django.views import View

from logging import getLogger

from tournaments.forms import ClubForm, PlayerForm
from tournaments.models import Club, Player

LOGGER = getLogger()

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


class PlayersView(TemplateView):
    template_name = 'tournaments/players.html'
    extra_context = {'players': Player.objects.all()}

# Tady mam problem dostat tam context, nemuzu spravne zalozit hrace / zobrazit
def player(request, pk):
    player = Player.objects.all()
    context = {}
    return render(request, template_name='tournaments/player.html', context=context)

class PlayerCreateView(CreateView):
    template_name = 'tournaments/player_form.html'
    extra_context = {'title':'Create new player'}
    form_class = PlayerForm
    success_url = reverse_lazy('players')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)

class PlayerUpdateView(UpdateView):
    template_name = 'tournaments/playe_form.html'
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('players')

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)

class PlayerDeleteView(DeleteView):
    template_name = 'tournaments/player_delete.html'
    model = Player
    success_url = reverse_lazy('players')


# odobny problem jako u Player
def club(request, pk):
    club = Club.objects.get(id=pk)

    if request.method == "POST":
        return redirect('club', pk)

    return render(request, template_name='tournament/club.html', context=context)

    clubs = club_set.all()

    context = {'clubs': clubs}
    return render(request, template_name='tournaments/club.html', context=context)


class ClubCreateView(CreateView):
    template_name = 'tournament/club_form.html'
    extra_context = {'title' : 'Create new club'}
    form_class = Club
    success_url = reverse_lazy('clubs')

    def form_valid(self, form):
        result = super().form_valid(form)
        return result

class ClubsView(ListView):
    template_name = 'tournaments/clubs.html'
    model = Club
