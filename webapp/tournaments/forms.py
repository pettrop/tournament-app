from django.core.exceptions import ValidationError
from django.forms import (
    ModelForm, CharField, DateField, IntegerField, ModelChoiceField, ModelMultipleChoiceField, SelectDateWidget)

from tournaments.models import Club, Player, Propositions, Category, League, Discipline, Schedule, Season, Organizer
    ModelForm, CharField, DateField, IntegerField, EmailField)


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    name = CharField(max_length=32)
    lastname = CharField(max_length=32)
    year_of_birth = IntegerField()
    license_validity = DateField()

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.capitalize()

    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        return lastname.capitalize()

    def clean(self):
        result = super().clean()
        return result


class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = '__all__'

    club_name = CharField(max_length=64)

    def clean_club_name(self):
        club_name = self.cleaned_data['club_name']
        return club_name.capitalize()

    def clean(self):
        result = super().clean()
        return result


class SeasonForm(ModelForm):
    class Meta:
        model = Season
        fields = '__all__'

    season_name = CharField(max_length=64)

    def clean_season_name(self):
        season_name = self.cleaned_data['season_name']
        return season_name.capitalize()

    def clean(self):
        result = super().clean()
        return result


class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = '__all__'

    league_name = CharField(max_length=32)

    def clean_league_name(self):
        league_name = self.cleaned_data['league_name']
        return league_name.capitalize()

    def clean(self):
        result = super().clean()
        return result


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    category_name = CharField(max_length=32)

    def clean_category_name(self):
        category_name = self.cleaned_data['category_name']
        return category_name.capitalize()

    def clean(self):
        result = super().clean()
        return result


class DisciplineForm(ModelForm):
    class Meta:
        model = Discipline
        fields = '__all__'

    discipline_name = CharField(max_length=32)

    def clean_discipline_name(self):
        discipline_name = self.cleaned_data['discipline_name']
        return discipline_name.capitalize()

    def clean(self):
        result = super().clean()
        return result


class OrganizerForm(ModelForm):
    class Meta:
        model = Organizer
        fields = '__all__'

    organizer_name = CharField(max_length=32)
    organizer_lastname = CharField(max_length=32)
    organizer_mail = EmailField()
    organizer_phone = CharField(max_length=14)

    def clean_organizer_name(self):
        organizer_name = self.cleaned_data['organizer_name']
        return organizer_name.capitalize()

    def clean_organizer_lastname(self):
        organizer_lastname = self.cleaned_data['organizer_lastname']
        return organizer_lastname.capitalize()

    def clean(self):
        result = super().clean()
        return result



class PropositionForm(ModelForm):
    class Meta:
        model = Propositions
        fields = ['prescription', 'tournament_system', 'notes', 'category', 'league', 'discipline', 'event_location',
                  'event_date', 'schedule', 'season', 'tournament_order', 'organizer_club', 'director', 'judge', 'registration']
        widgets = {
            'event_date': SelectDateWidget()
        }

    category = ModelMultipleChoiceField(queryset=Category.objects.all())
    league = ModelMultipleChoiceField(queryset=League.objects.all())
    discipline = ModelMultipleChoiceField(queryset=Discipline.objects.all())
    schedule = ModelMultipleChoiceField(queryset=Schedule.objects.all())
    season = ModelChoiceField(queryset=Season.objects.all())
