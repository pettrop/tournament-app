from django.db import models
from django.db.models import Model, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import forms
from django.urls import reverse
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Club(Model):
    club_name = models.CharField(max_length=64, unique=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):

        return '{} (id: {})'.format(self.club_name, self.id)

    class Meta:
        ordering = ['club_name']


class Category(Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return '{}'.format(self.category_name)


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Player(Model):
    name = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    year_of_birth = models.IntegerField()
    license_validity = models.DateField()
    player_is_girl = models.BooleanField(default=False)
    club = models.ForeignKey(Club, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return '{} {} ({}, id: {})'.format(self.lastname, self.name, self.year_of_birth, self.id)

    class Meta:
        ordering = ['lastname']
        unique_together = (('name', 'lastname', 'year_of_birth'),)


class Season(Model):
    season_name = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.season_name


class League(Model):
    league_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.league_name


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

    class Meta:
        ordering = ['organizer_lastname']
        unique_together = (('organizer_name', 'organizer_lastname', 'organizer_mail', 'organizer_phone'),)


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

    class Meta:
        ordering = ['event_date']
        unique_together = (('event_location', 'event_date', 'organizer_club'),)


class Scoreboard(Model):
    ranking_points = models.JSONField()

    def __str__(self):
        return 'Bodovacia tabuľka {}'.format(self.pk)


class Tournament(Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    propositions = models.ForeignKey(Propositions, on_delete=models.PROTECT, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,blank=True, null=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.name, self.category, self.propositions)

    def get_edit_url(self):
        return reverse("tournament:update", kwargs={"pk": self.pk})

    def get_result_children(self):
        return self.result_set.all()


class Result(Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    result = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.player)

@receiver(post_save, sender=Result)
def update_player_rank(sender, instance, **kwargs):
    tournament = instance.tournament
    results = Result.objects.filter(tournament=tournament).order_by('-result')
    rank = 1
    for result in results:
        result.player.rank = rank
        result.player.save()
        rank += 1