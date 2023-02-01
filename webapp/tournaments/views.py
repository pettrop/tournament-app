from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import DatabaseError
from django.db.models import ProtectedError, Count
from django.db.models import Sum
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

import datetime
from django.contrib.messages.views import SuccessMessageMixin

from logging import getLogger

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
    paginate_by = 20


def player(request, pk):
    player = Player.objects.get(pk=pk)
    context = {'player': player}
    return render(request, template_name='tournaments/player.html', context=context)


class PlayerCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/player_form.html'
    extra_context = {'title': 'Vytvor hráča'}
    form_class = PlayerForm
    success_message = 'Hráč bol úspešne vytvorený'
    success_url = reverse_lazy('players')
    permission_required = ['tournaments.add_player']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided')
        return super().form_invalid(form)


class PlayerUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/player_form.html'
    extra_context = {'title': 'Uprav hráče'}
    model = Player
    form_class = PlayerForm
    success_message = 'Úprava údajov prebehla v poriadku'
    success_url = reverse_lazy('players')
    permission_required = ['tournaments.change_player']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class PlayerDeleteView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/player_delete.html'
    model = Player
    success_message = 'Hráč bol zmazaný'
    success_url = reverse_lazy('players')
    permission_required = ['tournaments.delete_player']


# Club/Clubs

def club(request, pk):
    club = Club.objects.get(pk=pk)
    players = club.player_set.all()
    context = {'club': club,
               'players': players}
    return render(request, template_name='tournaments/club.html', context=context)


class ClubCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/club_form.html'
    extra_context = {'title': 'Vytvor nový klub'}
    model = Club
    form_class = ClubForm
    success_message = 'Klub bol úspešne vytvorený'
    success_url = reverse_lazy('clubs')
    permission_required = ['tournaments.add_club']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class ClubUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/club_form.html'
    extra_context = {'title': 'Uprav klub'}
    model = Club
    form_class = ClubForm
    success_message = 'Úprava údajov prebehla v poriadku'
    success_url = reverse_lazy('clubs')
    permission_required = ['tournaments.change_club']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class ClubDeleteView(SuccessMessageMixin, DatabaseError, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/club_delete.html'
    model = Club
    success_message = 'Klub bol zmazaný'
    success_url = reverse_lazy('clubs')
    permission_required = ['tournaments.delete_club']

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, "Klub nemôže byť zmazaný, pretože má už priradených hráčov")
        else:
            messages.success(self.request, "Klub bol zmazaný")
        return redirect(success_url)

class ClubsView(ListView):
    template_name = 'tournaments/clubs.html'
    model = Club
    paginate_by = 20


# Season / Seasons

def season(request, pk):
    season = Season.objects.get(pk=pk)

    context = {'season': season}
    return render(request, template_name='tournaments/season.html', context=context)


class SeasonsView(ListView):
    template_name = 'tournaments/seasons.html'
    model = Season


class SeasonCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/season_form.html'
    extra_context = {'title': 'Vytvor sezónu'}
    model = Season
    form_class = SeasonForm
    success_message = 'sezóna bola úspešne vytvorená'
    success_url = reverse_lazy('seasons')
    permission_required = ['tournaments.add_season']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class SeasonUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/season_form.html'
    extra_context = {'title': 'Uprav sezonu'}
    model = Season
    form_class = SeasonForm
    success_message = 'Úprava údajov prebehla v poriadku'
    success_url = reverse_lazy('seasons')
    permission_required = ['tournaments.change_season']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class SeasonDeleteView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/season_delete.html'
    model = Season
    success_message = 'sezóna bola zmazaná'
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


class LeagueCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/league_form.html'
    extra_context = {'title': 'Vytvor novú ligu'}
    model = League
    form_class = LeagueForm
    success_message = 'Liga bola vytvorená'
    success_url = reverse_lazy('leagues')
    permission_required = ['tournaments.add_league']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class LeagueUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/league_form.html'
    extra_context = {'title': 'Uprav ligu'}
    model = League
    form_class = LeagueForm
    success_message = 'Úprava údajov prebehla v poriadku'
    success_url = reverse_lazy('leagues')
    permission_required = ['tournaments.change_league']

    def form_invalid(self, form):
        LOGGER.warning('invalid data provided while updating')
        return super().form_invalid(form)


class LeagueDeleteView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/league_delete.html'
    model = League
    success_message = 'Liga bola zmazaná'
    success_url = reverse_lazy('leagues')
    permission_required = ['tournaments.delete_league']


# Category / Categories

def category(request, pk):
    #TODO zatial natvrdo zadane radenie do kategorie!
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


class CategoryCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Vytvor novú kategóriu'}
    model = Category
    form_class = CategoryForm
    success_message = 'Kategória bola vytvorená'
    success_url = reverse_lazy('categories')
    permission_required = ['tournaments.add_category']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class CategoryUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/category_form.html'
    extra_context = {'title': 'Uprav kategorii'}
    model = Category
    form_class = CategoryForm
    success_message = 'Úprava údajov prebehla v poriadku'
    success_url = reverse_lazy('categories')
    permission_required = ['tournaments.change_category']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result



class CategoryDeleteView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/category_delete.html'
    model = Category
    success_message = 'Kategória bola zmazaná'
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


class DisciplineCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/discipline_form.html'
    extra_context = {'title': 'Vytvor novú disciplínu'}
    model = Discipline
    form_class = DisciplineForm
    success_message = 'Disciplína bola vytvorená'
    success_url = reverse_lazy('disciplines')
    permission_required = ['tournaments.add_discipline']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class DisciplineUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/discipline_form.html'
    extra_context = {'title': 'Uprav disciplínu'}
    model = Discipline
    form_class = DisciplineForm
    success_message = 'Úprava údajov prebehla v poriadku'
    success_url = reverse_lazy('disciplines')
    permission_required = ['tournaments.change_discipline']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class DisciplineDeleteView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/discipline_delete.html'
    model = Discipline
    success_message = 'Disciplína bola zmazaná'
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


class OrganizerCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'tournaments/organizer_form.html'
    extra_context = {'title': 'Vytvor organizátora'}
    model = Organizer
    form_class = OrganizerForm
    success_message = 'Organizátor bol úspešne vytvorený'
    success_url = reverse_lazy('organizers')
    permission_required = ['tournaments.add_organizer']

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class OrganizerUpdateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'tournaments/organizer_form.html'
    extra_context = {'title': 'Uprav organizátora'}
    model = Organizer
    form_class = OrganizerForm
    success_message = 'Úprava údajov prebehla v poriadku'
    success_url = reverse_lazy('organizers')
    permission_required = ['tournaments.change_organizer']

    def form_invalid(self, form):
        LOGGER.warning('Invalid data provided while updating')
        return super().form_invalid(form)


class OrganizerDeleteView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'tournaments/organizer_delete.html'
    model = Organizer
    success_message = 'Organizátor bol zmazaný'
    success_url = reverse_lazy('organizers')
    context_object_name = 'clubs'
    # ordering = ['-name']
    permission_required = ['tournaments.delete_organizer']


class PropositionsView(ListView):
    model = Propositions
    template_name = 'tournaments/propositions.html'
    context_object_name = 'propositions'
    paginate_by = 10
    ordering = ['-event_date']


class PropositionCreateView(SuccessMessageMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Propositions
    form_class = PropositionForm
    template_name = 'tournaments/proposition_create.html'
    success_message = 'Propozícia bola úspešne vytvorená'
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

class PropositionDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'tournaments/proposition_delete.html'
    model = Propositions
    success_message = 'Propozícia bola zmazaná'
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
        #TODO Upravit presmerovanie/nacitanie stranky pri vytvarani turnajov
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
            messages.success(request, 'Zmeny boli uložené!')
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
    # vycet vsetkych hracov turnaja
    results_players = Result.objects.filter(tournament_id=pk)

    # nacitanie kategorie turnaja
    tournament = Tournament.objects.get(id=pk)

    # vypis poctu hracov v jednotlivych kluboch
    player_count_in_club = Result.objects.filter(tournament_id=pk).values('player__club__id').annotate(player_count=Count('player')).filter(player_count__gte=2)
    #print(player_count_in_club)

    # vytvorenie zoznamu zucastnenych klubov na turnaji
    club_ids = set()
    for club in player_count_in_club:
        club_ids.add(club['player__club__id'])
    #print(club_ids)

    clubs_score = dict()
    clubs_score_sorted = dict()
    for club_id in club_ids:
        club = Club.objects.get(id=club_id)
        #print("CLUB:", club)

        scores_players_club = []
        # toto vypise vsetkych hracov z klubu
        # print(club.player_set.all())
        # prejdenie cyklom for pre zistenie, ci dany hrac hral na danom turnaji, ak ano zapise jeho vysledky do pola
        for player in club.player_set.all():
            try:
                player_result = Result.objects.get(player=player, tournament_id=pk)
            except Result.DoesNotExist:
                continue
            scores_players_club.append((player, player_result.result))
        #print("SCORE before sort:", scores_players_club)

        # zoradenie a vyber prvych troch najlepsich hracov z klubu
        top_3_players = sorted(scores_players_club, key=lambda x: x[1], reverse=True)[:3]
        #print("BEST 3 PLAYERS:", top_3_players)

        # sucet bodov troch najlepsich hracov z klubu
        tournament_club_score = sum(map(lambda x: x[1], top_3_players))
        #print("CLUB Score:", tournament_club_score)

        # zapisanie vysledkov do slovnika s klucom nazvom klubu napr. POZOR nezoradene! {'TTC Spartak Poprad': 352, 'TJ Dunajec Spišská Stará Ves': 216, '1. PPC Fortuna Kežmarok': 173, 'STO Mladý pinpongista Slovenská Ves': 159, 'STO Slovenská Ves': 120}
        if club.club_name in clubs_score:
            clubs_score[club.club_name] += tournament_club_score
        else:
            clubs_score[club.club_name] = tournament_club_score

        # zoradenie hodnot vysledkov klubov
        clubs_score_sorted = dict(sorted(clubs_score.items(), key=lambda item: item[1], reverse=True))
        #print(clubs_score_sorted)

    context = {
        'results_players': results_players,
        'tournament': tournament,
        'clubs_score_sorted': clubs_score_sorted
    }
    return render(request, template_name="tournaments/results_detail.html", context=context)



def results_total(request, season_pk=None, category_pk=None):
    season = Season.objects.get(pk=season_pk) #vypise sezonu podla pk => 2022/2023
    category_name = Category.objects.get(id=category_pk) #starší žiaci
    tournaments = Tournament.objects.filter(propositions__season__season_name=season, category=category_pk) #<QuerySet [<Tournament: Turnaj 1 - starší žiaci (2022-10-15 - Telocvičňa ZŠ Spišský Štvrtok (2022/2023))>]>
    #print("Tournaments:", tournaments)
    tournaments_count = int(len(tournaments)) #vypise pocet turnajov cislom, napr. 1, 2
    #print("POCET TURNAJOV:", tournaments_count)

    season_sum_score_category = dict()
    season_sum_score_category_sorted = dict()
    for tournament in tournaments:

        #print("TURNAMENTY:", tournament) #postupne vypisuej nazvy turnajov: Turnaj 1 - starší žiaci (2022-10-15 - Telocvičňa ZŠ Spišský Štvrtok (2022/2023))
        result_data = Result.objects.filter(tournament=tournament).values('player__club__id', 'tournament').annotate(player_count=Count('player')).filter(player_count__gte=2)
        print("Result data:", result_data)
        club_ids = set()

        for result in result_data:
            #print("RESULT", result)
            club_id = result['player__club__id']
            club_ids.add(club_id)
        print("IDcka KLUBOV:", club_ids)

        for club_id in club_ids:
            club = Club.objects.get(id=club_id)
            #print("CLUB:", club)

            scores = []
            for player in club.player_set.all():
                #print("Player:", player)
                try:
                    tresult = Result.objects.get(player=player, tournament=tournament)
                    #print("tresult", tresult)
                except Exception: #upravit zachytenie iba chyby DoesNotExist!
                    continue
                #print("TRESULT", tresult.result)
                scores.append((player, tresult.result))
            top_3_players = sorted(scores, key=lambda x: x[1], reverse=True)[:3]
            print("TOP", top_3_players)
            tournament_sum_score = sum( map(lambda x: x[1], top_3_players) )
            print("SUMA", tournament_sum_score)
            if club.club_name in season_sum_score_category:
                season_sum_score_category[club.club_name] += tournament_sum_score
            else:
                season_sum_score_category[club.club_name] = tournament_sum_score
    print(season_sum_score_category)
    season_sum_score_category_sorted = dict(sorted(season_sum_score_category.items(), key=lambda item: item[1], reverse=True))

    context = {
        'category_name': category_name,
        'tournaments_count': tournaments_count,
        'tournaments': tournaments,
        'season_sum_score_category': season_sum_score_category_sorted,
        'season': season,
    }
    return render(request, template_name="tournaments/results_total_category.html", context=context)


def seasons_views(request):
    seasons_list = Season.objects.all()
    print(seasons_list)
    context = {
        'seasons_list': seasons_list
    }
    return render(request, template_name='tournaments/results_seasons_list.html', context=context)


def season_category_view(request, season_pk=None):

    tournaments_season = Tournament.objects.filter(propositions__season__id=season_pk)
    category_season = Category.objects.filter(tournament__result__isnull=False).annotate(tournament_count=Count('tournament')).filter(tournament_count__gt=0)
    season_name = Season.objects.get(id=season_pk)
    print(season_name)
    context = {
        'season_name': season_name,
        'season': season_pk,
        'tournament_season': tournaments_season,
        'category_season': category_season
    }
    return render(request, template_name='tournaments/season_category.html', context=context)


def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler404(request, exception):
    return render(request, '404.html', status=404)

# def error_404(request, exception):
#    context = {}
#    return render(request,'404.html', context)


#TODO dorobit views pre rozvrh - schedule turnajov