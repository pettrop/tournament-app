from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

import datetime


from logging import getLogger, Logger

from tournaments.forms import ClubForm, PlayerForm, SeasonForm, LeagueForm, CategoryForm, DisciplineForm, OrganizerForm, \
    PropositionForm, TournamentForm, ResultsAddForm
from tournaments.models import Club, Player, Season, League, Category, Discipline, Organizer, Propositions, Tournament, \
    Result

LOGGER = getLogger()


def home(request):
    template = "home.html"
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


class PlayerCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/player_form.html'
    extra_context = {'title': 'Vytvoř hráče'}
    form_class = PlayerForm
    success_url = reverse_lazy('players')
    permission_required = ['tournaments.add_player']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided')
        return super().form_invalid(form)


class PlayerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/player_form.html'
    extra_context = {'title': 'Uprav hráče'}
    model = Player
    form_class = PlayerForm
    success_url = reverse_lazy('players')
    permission_required = ['tournaments.change_player']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class PlayerDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/player_delete.html'
    model = Player
    success_url = reverse_lazy('players')
    permission_required = ['tournaments.delete_player']


# Club/Clubs

def club(request, pk):
    club = Club.objects.get(pk=pk)
    players = club.player_set.all()
    context = {'club': club,
               'players': players}
    return render(request, template_name='tournaments/club.html', context=context)


class ClubCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/club_form.html'
    extra_context = {'title': 'Vytvoř nový klub'}
    model = Club
    form_class = ClubForm
    success_url = reverse_lazy('clubs')
    permission_required = ['tournaments.add_club']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result



class ClubUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/club_form.html'
    extra_context = {'title': 'Uprav klub'}
    model = Club
    form_class = ClubForm
    success_url = reverse_lazy('clubs')
    permission_required = ['tournaments.change_club']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class ClubDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/club_delete.html'
    model = Club
    success_url = reverse_lazy('clubs')
    permission_required = ['tournaments.delete_club']


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


class SeasonCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/season_form.html'
    extra_context = {'title': 'Vytvoř sezonu'}
    model = Season
    form_class = SeasonForm
    success_url = reverse_lazy('seasons')
    permission_required = ['tournaments.add_season']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class SeasonUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/season_form.html'
    extra_context = {'title': 'Uprav sezonu'}
    model = Season
    form_class = SeasonForm
    success_url = reverse_lazy('seasons')
    permission_required = ['tournaments.change_season']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class SeasonDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/season_delete.html'
    model = Season
    success_url = reverse_lazy('seasons')
    permission_required = ['tournaments.delete_season']


# League / Leagues

def league(request, pk):
    league = League.objects.get(pk=pk)
    context = {'league': league}
    return render(request, template_name='tournaments/league.html', context=context)


class LeaguesView(ListView):
    template_name = 'tournaments/leagues.html'
    model = League


class LeagueCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/league_form.html'
    extra_context = {'title': 'Vytvoř novou ligu'}
    model = League
    form_class = LeagueForm
    success_url = reverse_lazy('leagues')
    permission_required = ['tournaments.add_league']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class LeagueUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/league_form.html'
    extra_context = {'title': 'Uprav ligu'}
    model = League
    form_class = LeagueForm
    success_url = reverse_lazy('leagues')
    permission_required = ['tournaments.change_league']

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)


class LeagueDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/league_delete.html'
    model = League
    success_url = reverse_lazy('leagues')
    permission_required = ['tournaments.delete_league']


# Category / Categories

def category(request, pk):
    category = Category.objects.get(pk=pk)
    current_year = datetime.date.today().year
    all_players = Player.objects.all()
    players_dospeli = []
    players_dorastenci = []
    players_starší_žiaci = []
    players_mladší_žiaci = []
    players_ostatni = []
    players_dievčata = []
    for player in all_players:
        if player.player_is_girl is True:
            players_dievčata.append(player)
        else:
            if (current_year - 20) >= player.year_of_birth:
                players_dospeli.append(player)
            elif (current_year - 15) > player.year_of_birth and player.year_of_birth >= (current_year - 19):
                players_dorastenci.append(player)
            elif (current_year - 13) > player.year_of_birth and player.year_of_birth >= (current_year - 15):
                players_starší_žiaci.append(player)
            elif player.year_of_birth >= (current_year - 13):
                players_mladší_žiaci.append(player)
            else: players_ostatni.append(player)

    context = {'category': category,
               'players_dospeli': players_dospeli,
               'players_dorastenci': players_dorastenci,
               'players_starší_žiaci': players_starší_žiaci,
               'players_mladší_žiaci': players_mladší_žiaci,
               'players_ostatni': players_ostatni,
               'players_dievčata': players_dievčata}
    print(context)
    return render(request, template_name='tournaments/category.html', context=context)

class CategoriesView(ListView):
    template_name = 'tournaments/categories.html'
    model = Category


class CategoryCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Vytvoř novou kategorii'}
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('categories')
    permission_required = ['tournaments.add_category']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class CategoryUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Uprav kategorii'}
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('categories')
    permission_required = ['tournaments.change_category']

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)


class CategoryDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/category_delete.html'
    model = Category
    success_url = reverse_lazy('categories')
    permission_required = ['tournaments.delete_category']


# Discipline / Disciplines asi neni spravne anglicky, ale potrebuji odlisit mnozne cislo

def discipline(request, pk):
    discipline = Discipline.objects.get(pk=pk)
    context = {'discipline': discipline}
    return render(request, template_name='tournaments/discipline.html', context=context)


class DisciplinesView(ListView):
    template_name = 'tournaments/disciplines.html'
    model = Discipline


class DisciplineCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/discipline_form.html'
    extra_context = {'title': 'Vytvoř novou disciplínu'}
    model = Discipline
    form_class = DisciplineForm
    success_url = reverse_lazy('disciplines')
    permission_required = ['tournaments.add_discipline']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class DisciplineUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/discipline_form.html'
    extra_context = {'title': 'Uprav disciplínu'}
    model = Discipline
    form_class = DisciplineForm
    success_url = reverse_lazy('disciplines')
    permission_required = ['tournaments.change_discipline']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class DisciplineDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/discipline_delete.html'
    model = Discipline
    success_url = reverse_lazy('disciplines')
    permission_required = ['tournaments.delete_discipline']


# Organizer / Organizers

def organizer(request, pk):
    organizer = Organizer.objects.get(pk=pk)
    context = {'organizer': organizer}
    return render(request, template_name='tournaments/organizer.html', context=context)


class OrganizersView(ListView):
    template_name = 'tournaments/organizers.html'
    model = Organizer


class OrganizerCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/organizer_form.html'
    extra_context = {'title': 'Vytvoř organizátora'}
    model = Organizer
    form_class = OrganizerForm
    success_url = reverse_lazy('organizers')
    permission_required = ['tournaments.add_organizer']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class OrganizerUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/organizer_form.html'
    extra_context = {'title': 'Uprav organizátora'}
    model = Organizer
    form_class = OrganizerForm
    success_url = reverse_lazy('organizers')
    permission_required = ['tournaments.change_organizer']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class OrganizerDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/organizer_delete.html'
    model = Organizer
    success_url = reverse_lazy('organizers')
    context_object_name = 'clubs'
    # ordering = ['-name']
    permission_required = ['tournaments.delete_organizer']


class PropositionsView(ListView):
    model = Propositions
    template_name = 'tournaments/propositions.html'
    context_object_name = 'propositions'
    paginate_by = 5
    ordering = ['-event_date']


class PropositionCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Propositions
    form_class = PropositionForm
    template_name = 'tournaments/proposition_create.html'
    success_url = reverse_lazy('propositions')
    extra_context = {'title': 'Vytvor propozíciu'}
    permission_required = ['tournaments.add_propositions']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def proposition_detail(request, pk):
    proposition = Propositions.objects.get(pk=pk)
    league_prop = proposition.league.all()
    disciplines = proposition.discipline.all()
    categories = proposition.category.all()
    schedules = proposition.schedule.all()

    context = {
        'proposition': proposition,
        'leagues': league_prop,
        'disciplines': disciplines,
        'categories': categories,
        'schedules': schedules,
    }
    return render(request, template_name='tournaments/proposition_detail.html', context=context)

class PropositionDeleteView(DeleteView):
    template_name = 'tournaments/proposition_delete.html'
    model = Propositions
    success_url = reverse_lazy('propositions')
    context_object_name = 'propositions'


@login_required
@permission_required(['tournaments.add_tournament'])
def tournament_create_view(request):
    form = TournamentForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save()
        return redirect('tournaments')

    return render(request, template_name='tournaments/tournament_create_update.html', context=context)


def tournament_list_view(request):
    tournaments_list = Tournament.objects.all()
    context = {
        "tournaments_list": tournaments_list
    }
    return render(request, template_name="tournaments/tournaments.html", context=context)

@login_required
@permission_required(['tournaments.change_tournament'])
def tournament_update_view(request, pk):
    obj = get_object_or_404(Tournament, pk=pk)
    form = TournamentForm(request.POST or None, instance=obj)
    ResultsFormset = modelformset_factory(Result, form=ResultsAddForm, extra=0)
    qs = obj.result_set.all()
    formset = ResultsFormset(request.POST or None, queryset=qs)

    context = {
        "form": form,
        "formset": formset,
        "object": obj,
    }


    if all([form.is_valid(), formset.is_valid()]):
            parent = form.save(commit=False)
            parent.save()
            for form in formset:
                child = form.save(commit=False)
                child.tournament = parent
                child.save()
            context['message'] = 'Data saved.'
    return render(request, template_name="tournaments/tournament_create_update.html", context=context)


def tournament_detail_view(request, pk=None):
    obj = get_object_or_404(Tournament, pk=pk)
    context = {
        "object": obj
    }
    return render(request, "tournaments/tournament_detail.html", context)


def results_view(request):
    tournaments_list = Tournament.objects.all()
    context = {
        "tournaments_list": tournaments_list
    }
    return render(request, template_name="tournaments/results.html", context=context)


def results_detail(request, pk=None):
    results_players = Result.objects.filter(tournament_id=pk).values('player_id', 'player__name', 'player__lastname', 'player__year_of_birth', 'player__club__club_name').annotate(points=Sum('result')).order_by('-points')
    club_names = Result.objects.filter(tournament_id=pk).values('player__club__club_name').distinct()
    results_club = []
    for club_name in club_names:
        club = club_name["player__club__club_name"]
        top_three_players = Result.objects.filter(tournament_id=pk,
                                                  player__club__club_name=club_name["player__club__club_name"]).values(
            'player_id', 'player__name', 'player__lastname').annotate(points=Sum('result')).order_by('-points')[:3]
        sum_points_club = sum([player['points'] for player in top_three_players])
        results_club.extend([(club, sum_points_club)])

    results_club_ordered = sorted(results_club, key=lambda item: item[1], reverse=True)

    context = {
        "results_club_ordered": results_club_ordered,
        "results_players": results_players
    }
    return render(request, template_name="tournaments/results_detail.html", context=context)



def handler403(request, exception):
    return render(request, '403.html', status=403)
