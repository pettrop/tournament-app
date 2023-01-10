from django.contrib import admin
from .models import Tournament, Propositions, Schedule, Organizer, Function, Discipline, Category, League, Season, Player, Club, Results

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Propositions)
admin.site.register(Schedule)
admin.site.register(Organizer)
admin.site.register(Function)
admin.site.register(Discipline)
admin.site.register(Category)
admin.site.register(League)
admin.site.register(Season)
admin.site.register(Player)
admin.site.register(Club)
admin.site.register(Results)
