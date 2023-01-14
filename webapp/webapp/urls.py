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

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, TemplateView
from django.urls import path
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import defaulttags

import accounts.views
import tournaments.views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', tournaments.views.main_view, name='homepage'),
    
    path('results/', tournaments.views.results, name="results"),
    
    path('accounts/signup/', accounts.views.signup, name='signup'),
    path('accounts/login/', accounts.views.custom_login, name='login'),
    path('accounts/logout/', accounts.views.custom_logout, name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name="registration/password_change.html"), name='password_change'),
    path('accounts/password_change/done', PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name='password_change_done'),
    path('accounts/signup_successful/', accounts.views.signupsuccessful, name='signupsuccessful'),

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

]
