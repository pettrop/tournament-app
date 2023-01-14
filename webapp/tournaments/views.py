from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView
from django.template import defaulttags
from django.views import View

from logging import getLogger, Logger

from tournaments.forms import ClubForm, PlayerForm, SeasonForm
from tournaments.models import Club, Player, Season

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

#Player / Players
class PlayersView(TemplateView):
    template_name = 'tournaments/players.html'
    extra_context = {'players': Player.objects.all()}


def player(request, pk):
    player = Player.objects.get(pk=pk)
    context = {'player': player}
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
    template_name = 'tournaments/player_form.html'
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


# Club/Clubs
def club(request, pk):
        club = Club.objects.get(pk=pk)
        context = {'club': club}
        return render(request, template_name='tournaments/club.html', context=context)


class ClubCreateView(CreateView):
    template_name = 'tournaments/club_form.html'
    extra_context = {'title' : 'Create new club'}
    model = Club
    form_class = ClubForm
    success_url = reverse_lazy('clubs')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)

class ClubUpdateView(UpdateView):
    template_name = 'tournaments/club_form.html'
    model = Club
    form_class = ClubForm
    success_url = reverse_lazy('clubs')

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)
class ClubDeleteView(DeleteView):
    template_name = 'tournaments/club_delete.html'
    model = Club
    success_url = reverse_lazy('clubs')

class ClubsView(TemplateView):
    template_name = 'tournaments/clubs.html'
    extra_context = {'clubs': Club.objects.all()}

# Season / Seasons

def season(request, pk):
    season = Season.objects.get(pk=pk)
    context = {'season': season}
    return render(request, template_name='tournaments/season.html', context=context)
class SeasonsView(TemplateView):
    template_name = 'tournaments/seasons.html'
    extra_context = {'seasons': Season.objects.all()}

class SeasonCreateView(CreateView):
    template_name = 'tournaments/season_form.html'
    extra_context = {'title': 'Create new season'}
    model = Season
    form_class = SeasonForm
    success_url = reverse_lazy('seasons')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)

class SeasonUpdateView(UpdateView):
    template_name = 'tournaments/season_form.html'
    model = Season
    form_class = SeasonForm
    success_url = reverse_lazy('seasons')

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)
class SeasonDeleteView(DeleteView):
    template_name = 'tournaments/season_delete.html'
    model = Season
    success_url = reverse_lazy('seasons')