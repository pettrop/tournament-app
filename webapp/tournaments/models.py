import json

from django.db import models
from django.db.models import (
    CharField, DateTimeField, ForeignKey, IntegerField, TextField, DO_NOTHING, Model)
from django.template.defaultfilters import truncatechars
from django.template import defaulttags
from django.contrib.auth.models import User


# Create your models here.
class Club(Model):
    club_name = models.CharField(max_length=64)

    # # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.club_name
    # class Meta:
    #     ordering = ['club_name']


class Player(Model):
    name = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    # year_of_birth = models.IntegerField()
    year_of_birth = models.PositiveSmallIntegerField(blank=True)
    license_validity = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{} {} ({})'.format(self.lastname, self.name, self.year_of_birth)

    class Meta:
        ordering = ['lastname']


class Season(Model):
    season_name = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.season_name


class League(Model):
    league_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.league_name


class Category(Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Discipline(Model):
    discipline_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.discipline_name


class Organizer(Model):
    organizer_name = models.CharField(max_length=32)
    organizer_lastname = models.CharField(max_length=32)
    organizer_mail = models.EmailField(null=True)
    organizer_phone = models.CharField(max_length=14, null=True)

    def __str__(self):
        return '{} {} ({})'.format(self.organizer_lastname, self.organizer_name, self.organizer_mail)


class Schedule(Model):
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    task = models.TextField()

    def __str__(self):
        return '{} - {}: {}'.format(self.start_time.strftime('%H:%M'),
                                    self.end_time.strftime('%H:%M') if self.end_time else '',
                                    self.task[:30] + "..." if len(self.task) > 30 else self.task)


class Propositions(Model):
    prescription = models.TextField(null=True)
    tournament_system = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    league = models.ManyToManyField(League, blank=True)
    discipline = models.ManyToManyField(Discipline, blank=True)
    event_location = models.CharField(max_length=128, null=True)
    event_date = models.DateField(null=True)
    schedule = models.ManyToManyField(Schedule, blank=True)
    season = models.ForeignKey(Season, null=True, on_delete=models.PROTECT)
    tournament_order = models.PositiveSmallIntegerField(null=True, blank=True)
    organizer_club = models.ForeignKey(Club, null=True, on_delete=models.PROTECT)
    start_fee = models.PositiveSmallIntegerField(null=True, blank=True)
    director = models.ForeignKey(Organizer, null=True, blank=True, on_delete=models.PROTECT, related_name='director')
    judge = models.ForeignKey(Organizer, null=True, blank=True, on_delete=models.PROTECT, related_name='judge')
    registration = models.ForeignKey(Organizer, null=True, blank=True, on_delete=models.PROTECT,
                                     related_name='registration')

    def __str__(self):
        return '{} - {} ({})'.format(self.event_date, self.event_location, self.season)


class Scoreboard(Model):
    ranking_points = models.JSONField()

    def __str__(self):
        return 'Bodovacia tabuľka {}'.format(self.pk)


class Tournament(Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    propositions = models.ForeignKey(Propositions, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Result(Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    # ranking = models.ForeignKey(Scoreboard, on_delete=models.PROTECT)
    result = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.player)


def points_for_player_in_season(player_id):
    results = Result.objects.filter(player_id=player_id)
    total_result = 0
    for result in results:
        total_result += result.result
    return total_result


def points_for_club_in_tournament(tournament_id, club_id):
    results = Result.objects.filter(tournament_id=tournament_id).values('player__club_id').annotate(points=Sum('result')).filter(player__club_id=club_id)
    return results