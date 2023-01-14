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
    year_of_birth = models.PositiveSmallIntegerField()
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


class Function(Model):
    function_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.function_name

class Organizer(Model):
    organizer_name = models.CharField(max_length=32)
    organizer_lastname = models.CharField(max_length=32)
    function = models.ForeignKey(Function, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{} {} - {}'.format(self.organizer_lastname, self.organizer_name, self.function)


class Schedule(Model):
    start_time = models.TimeField()
    end_time = models.TimeField(null=True)
    task = models.TextField()

    def __str__(self):
        return '{} - {}: {}'.format(self.start_time.strftime('%H:%M'), self.end_time.strftime('%H:%M'), self.task[:30] + "..." if len(self.task) > 30 else self.task)


class Propositions(Model):
    prescription = models.TextField(null=True)
    tournament_system = models.TextField(null=True)
    notes = models.TextField(null=True)
    category = models.ManyToManyField(Category)
    league = models.ManyToManyField(League)
    discipline = models.ManyToManyField(Discipline)
    event_location = models.CharField(max_length=128, null=True)
    event_date = models.DateField(null=True, blank=True)
    schedule = models.ManyToManyField(Schedule, null=True)
    season = models.ForeignKey(Season, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{} - {} ({})'.format(self.season, str(self.league), self.category.name)


class Tournament(Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    tournament_order = models.PositiveSmallIntegerField(null=True)
    season = models.ForeignKey(Season, null=True, on_delete=models.DO_NOTHING)
    propositions = models.ForeignKey(Propositions, on_delete=models.DO_NOTHING, blank=True, null=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return '{} - {}'.format(self.name, self.season)


class Result(Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    score = models.PositiveSmallIntegerField()
    ranking = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} - {} ({}b)'.format(self.player, self.tournament, self.score)

