from django.contrib import admin
from .models import Tournament, Propositions, Schedule, Organizer, Discipline, Category, League, Season, \
    Player, Club, Result, Scoreboard

# Register your models here.

admin.site.register(Propositions)
admin.site.register(Schedule)
admin.site.register(Organizer)
admin.site.register(Discipline)
admin.site.register(Category)
admin.site.register(League)
admin.site.register(Season)
admin.site.register(Player)
admin.site.register(Club)
admin.site.register(Scoreboard)


class ResultsInline(admin.StackedInline):
    model = Result
    extra = 0


class TournamentAdmin(admin.ModelAdmin):
    inlines = [ResultsInline]


admin.site.register(Tournament, TournamentAdmin)
