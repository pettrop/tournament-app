from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView
from django.template import defaulttags
from django.views import View

from logging import getLogger, Logger

from tournaments.forms import ClubForm, PlayerForm, SeasonForm, LeagueForm, CategoryForm
from tournaments.models import Club, Player, Season, League, Category

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


# Player / Players
class PlayersView(ListView):
    template_name = 'tournaments/players.html'
    model = Player


def player(request, pk):
    player = Player.objects.get(pk=pk)
    context = {'player': player}
    return render(request, template_name='tournaments/player.html', context=context)


class PlayerCreateView(CreateView):
    template_name = 'tournaments/player_form.html'
    # extra_context = {'title':'Create new player'}
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

class ClubsView(ListView):
    template_name = 'tournaments/clubs.html'
    model = Club

# Season / Seasons

def season(request, pk):
    season = Season.objects.get(pk=pk)
    context = {'season': season}
    return render(request, template_name='tournaments/season.html', context=context)

class SeasonsView(ListView):
    template_name = 'tournaments/seasons.html'
    model = Season

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
    extra_context = {'title': 'Update season'}
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


# League / Leagues

def league(request, pk):
    league = League.objects.get(pk=pk)
    context = {'league': league}
    return render(request, template_name='tournaments/league.html', context=context)


class LeaguesView(ListView):
    template_name = 'tournaments/leagues.html'
    model = League


class LeagueCreateView(CreateView):
    template_name = 'tournaments/league_form.html'
    extra_context = {'title': 'Create new league'}
    model = League
    form_class = LeagueForm
    success_url = reverse_lazy('leagues')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class LeagueUpdateView(UpdateView):
    template_name = 'tournaments/league_form.html'
    extra_context = {'title': 'Update league {{ league.league_name}}'}
    model = League
    form_class = LeagueForm
    success_url = reverse_lazy('leagues')

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)


class LeagueDeleteView(DeleteView):
    template_name = 'tournaments/league_delete.html'
    model = League
    success_url = reverse_lazy('leagues')

# Category / Categories

def category(request, pk):
    category = Category.objects.get(pk=pk)
    context = {'category': category}
    return render(request, template_name='tournaments/category.html', context=context)


class CategoriesView(ListView):
    template_name = 'tournaments/categories.html'
    model = Category


class CategoryCreateView(CreateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Create new category'}
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('categories')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class CategoryUpdateView(UpdateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Update category {{ category.category_name}}'}
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('categories')

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)


class CategoryDeleteView(DeleteView):
    template_name = 'tournaments/category_delete.html'
    model = Category
    success_url = reverse_lazy('categories')