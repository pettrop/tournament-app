"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path

import accounts.views
import tournaments.views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', tournaments.views.home, name='home'),
    
    path('results/', tournaments.views.results, name="results"),
    
    path('accounts/signup/', accounts.views.signup, name='signup'),
    path('accounts/activate/<uidb64>/<token>/', accounts.views.activate, name='activate'),
    path('accounts/login/', accounts.views.custom_login, name='login'),
    path('accounts/logout/', accounts.views.custom_logout, name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name="registration/password_change.html"), name='password_change'),
    path('accounts/password_change/done', PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name='password_change_done'),
    path('accounts/password_reset/', accounts.views.password_reset_request, name='password_reset'),
    path('accounts/password_reset/<uidb64>/<token>', accounts.views.password_reset_confirm, name='password_reset_confirm'),
    path('accounts/profile/', accounts.views.profile, name='profile'),
    path('accounts/profile_update/', accounts.views.profile_update, name='profile_update'),
    path('accounts/permission_request/', accounts.views.permission_request, name='permission_request'),

    path('club/create', tournaments.views.ClubCreateView.as_view(), name='club_create'),
    path('club/update/<pk>', tournaments.views.ClubUpdateView.as_view(), name='club_update'),
    path('club/delete/<pk>', tournaments.views.ClubDeleteView.as_view(), name='club_delete'),
    path('club/detail/<pk>', tournaments.views.club, name='club'),
    path('clubs/', tournaments.views.ClubsView.as_view(), name='clubs'),

    path('player/detail/<pk>', tournaments.views.player, name='player'),
    path('player/create', tournaments.views.PlayerCreateView.as_view(), name='player_create'),
    path('player/update/<pk>', tournaments.views.PlayerUpdateView.as_view(), name='player_update'),
    path('player/delete/<pk>', tournaments.views.PlayerDeleteView.as_view(), name='player_delete'),
    path('players/', tournaments.views.PlayersView.as_view(), name='players'),

    path('season/detail/<pk>', tournaments.views.season, name='season'),
    path('season/create', tournaments.views.SeasonCreateView.as_view(), name='season_create'),
    path('season/update/<pk>', tournaments.views.SeasonUpdateView.as_view(), name='season_update'),
    path('season/delete/<pk>', tournaments.views.SeasonDeleteView.as_view(), name='season_delete'),
    path('seasons/', tournaments.views.SeasonsView.as_view(), name='seasons'),

    path('league/detail/<pk>', tournaments.views.league, name='league'),
    path('league/create', tournaments.views.LeagueCreateView.as_view(), name='league_create'),
    path('league/update/<pk>', tournaments.views.LeagueUpdateView.as_view(), name='league_update'),
    path('league/delete/<pk>', tournaments.views.LeagueDeleteView.as_view(), name='league_delete'),
    path('leagues/', tournaments.views.LeaguesView.as_view(), name='leagues'),

    path('category/detail/<pk>', tournaments.views.category, name='category'),
    path('category/create', tournaments.views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<pk>', tournaments.views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<pk>', tournaments.views.CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/', tournaments.views.CategoriesView.as_view(), name='categories'),

    path('discipline/detail/<pk>', tournaments.views.discipline, name='discipline'),
    path('discipline/create', tournaments.views.DisciplineCreateView.as_view(), name='discipline_create'),
    path('discipline/update/<pk>', tournaments.views.DisciplineUpdateView.as_view(), name='discipline_update'),
    path('discipline/delete/<pk>', tournaments.views.DisciplineDeleteView.as_view(), name='discipline_delete'),
    path('disciplines/', tournaments.views.DisciplinesView.as_view(), name='disciplines'),

    path('organizer/detail/<pk>', tournaments.views.organizer, name='organizer'),
    path('organizer/create', tournaments.views.OrganizerCreateView.as_view(), name='organizer_create'),
    path('organizer/update/<pk>', tournaments.views.OrganizerUpdateView.as_view(), name='organizer_update'),
    path('organizer/delete/<pk>', tournaments.views.OrganizerDeleteView.as_view(), name='organizer_delete'),
    path('organizers/', tournaments.views.OrganizersView.as_view(), name='organizers'),

    path('proposition/detail/<pk>', tournaments.views.proposition_detail, name='proposition'),
    path('proposition/create', tournaments.views.PropositionCreateView.as_view(), name='proposition_create'),
    path('propositions/', tournaments.views.PropositionsView.as_view(), name='propositions'),
    path('proposition/delete/<pk>', tournaments.views.PropositionDeleteView.as_view(), name='proposition_delete'),

    path('tournament/<int:pk>/edit', tournaments.views.tournament_update_view, name='tournament'),
    path('tournament/<int:pk>/', tournaments.views.tournament_detail_view),
    path('tournament/create', tournaments.views.tournament_create_view, name='tournament_create'),
    path('tournaments/', tournaments.views.tournament_list_view, name='tournaments'),



    #path('tournament/<int:tournament_id>/results/', tournaments.views.tournament_results, name='tournament_results'),
    #path('tournaments/', tournaments.views.TournamentsViews.as_view(), name='tournaments'),

    #path('results/add', tournaments.views.result_add, name='results_add'),
    #path('search_players/', tournaments.views.search_players, name='search_players'),
]
