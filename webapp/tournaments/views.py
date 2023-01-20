from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView


import datetime

from logging import getLogger, Logger

from tournaments.forms import ClubForm, PlayerForm, SeasonForm, LeagueForm, CategoryForm, DisciplineForm, OrganizerForm
from tournaments.models import Club, Player, Season, League, Category, Discipline, Organizer

LOGGER = getLogger()


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
    extra_context = {'title': 'Vytvoř hráče'}
    form_class = PlayerForm
    success_url = reverse_lazy('players')

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided')
        return super().form_invalid(form)


class PlayerUpdateView(UpdateView):
    template_name = 'tournaments/player_form.html'
    extra_context = {'title': 'Uprav hráče'}
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
    players = club.player_set.all()
    context = {'club': club,
               'players': players}
    return render(request, template_name='tournaments/club.html', context=context)

class ClubCreateView(CreateView):
    template_name = 'tournaments/club_form.html'
    extra_context = {'title': 'Vytvoř nový klub'}
    model = Club
    form_class = ClubForm
    success_url = reverse_lazy('clubs')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class ClubUpdateView(UpdateView):
    template_name = 'tournaments/club_form.html'
    extra_context = {'title': 'Uprav klub'}
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
    extra_context = {'title': 'Vytvoř sezonu'}
    model = Season
    form_class = SeasonForm
    success_url = reverse_lazy('seasons')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class SeasonUpdateView(UpdateView):
    template_name = 'tournaments/season_form.html'
    extra_context = {'title': 'Uprav sezonu'}
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
    extra_context = {'title': 'Vytvoř novou ligu'}
    model = League
    form_class = LeagueForm
    success_url = reverse_lazy('leagues')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class LeagueUpdateView(UpdateView):
    template_name = 'tournaments/league_form.html'
    extra_context = {'title': 'Uprav ligu'}
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
    current_year = datetime.date.today().year
    all_players = Player.objects.all()
    players_dospeli = []
    players_dorostenci = []
    players_starsi_zaci = []
    players_mladsi_zaci = []
    players_ostatni = []
    for player in all_players:
        if (current_year - 20) >= (player.year_of_birth):
            players_dospeli.append(player)
        elif (current_year - 18) >= (player.year_of_birth) and (player.year_of_birth) >= (current_year - 20):
            players_dorostenci.append(player)
        elif (current_year - 13) >= (player.year_of_birth) and (player.year_of_birth) >= (current_year - 18):
            players_starsi_zaci.append(player)
        elif (current_year - 10) >= (player.year_of_birth) and (player.year_of_birth) >= (current_year - 13):
            players_mladsi_zaci.append(player)
        else: players_ostatni.append(player)

    context = {'category': category,
               'players_dospeli': players_dospeli,
               'players_dorostenci': players_dorostenci,
               'players_starsi_zaci': players_starsi_zaci,
               'players_mladsi_zaci': players_mladsi_zaci,
               'players_ostatni': players_ostatni}
    return render(request, template_name='tournaments/category.html', context=context)

class CategoriesView(ListView):
    template_name = 'tournaments/categories.html'
    model = Category


class CategoryCreateView(CreateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Vytvoř novou kategorii'}
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('categories')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class CategoryUpdateView(UpdateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Uprav kategorii'}
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


# Discipline / Disciplines asi neni spravne anglicky, ale potrebuji odlisit mnozne cislo

def discipline(request, pk):
    discipline = Discipline.objects.get(pk=pk)
    context = {'discipline': discipline}
    return render(request, template_name='tournaments/discipline.html', context=context)


class DisciplinesView(ListView):
    template_name = 'tournaments/disciplines.html'
    model = Discipline


class DisciplineCreateView(CreateView):
    template_name = 'tournaments/discipline_form.html'
    extra_context = {'title': 'Vytvoř novou disciplínu'}
    model = Discipline
    form_class = DisciplineForm
    success_url = reverse_lazy('disciplines')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class DisciplineUpdateView(UpdateView):
    template_name = 'tournaments/discipline_form.html'
    extra_context = {'title': 'Uprav disciplínu'}
    model = Discipline
    form_class = DisciplineForm
    success_url = reverse_lazy('disciplines')

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)


class DisciplineDeleteView(DeleteView):
    template_name = 'tournaments/discipline_delete.html'
    model = Discipline
    success_url = reverse_lazy('disciplines')


# Organizer / Organizers

def organizer(request, pk):
    organizer = Organizer.objects.get(pk=pk)
    context = {'organizer': organizer}
    return render(request, template_name='tournaments/organizer.html', context=context)


class OrganizersView(ListView):
    template_name = 'tournaments/organizers.html'
    model = Organizer


class OrganizerCreateView(CreateView):
    template_name = 'tournaments/organizer_form.html'
    extra_context = {'title': 'Vytvoř organizátora'}
    model = Organizer
    form_class = OrganizerForm
    success_url = reverse_lazy('organizers')

    def form_invalid(self, form):
        Logger.warning('Invalid data provided')
        return super().form_invalid(form)


class OrganizerUpdateView(UpdateView):
    template_name = 'tournaments/organizer_form.html'
    extra_context = {'title': 'Uprav organizátora'}
    model = Organizer
    form_class = OrganizerForm
    success_url = reverse_lazy('organizers')

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)


class OrganizerDeleteView(DeleteView):
    template_name = 'tournaments/organizer_delete.html'
    model = Organizer
    success_url = reverse_lazy('organizers')
