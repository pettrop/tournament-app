from enum import unique

from django.core.exceptions import ValidationError
from django.db.models.functions import datetime
from django.forms import (ModelForm, CharField, DateField, IntegerField, ModelChoiceField, ModelMultipleChoiceField,
                          SelectDateWidget, EmailField, TextInput, forms, MultiWidget, Select, ChoiceField)


from tournaments.models import Club, Player, Propositions, Category, League, Discipline, Schedule, Season, Organizer, \
    Tournament, Result

from webapp import settings

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = '__all__'

    name = CharField(max_length=32)
    lastname = CharField(max_length=32)
    CHOICES = [(year, year) for year in range(1950, 2023)]
    year_of_birth = ChoiceField(widget=Select, choices=CHOICES)
    license_validity = DateField(
    widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
        months={
            1:'Január', 2:'Február', 3:'Marec', 4:'Apríl',
            5:'Máj', 6:'Jún', 7:'Júl', 8:'August',
            9:'September', 10:'Október', 11:'November', 12:'December'
        }
    ),
)
    def clean_name(self):
        name = self.cleaned_data['name']
        return name.capitalize()


    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        return lastname.capitalize()

    def clean(self):
        result = super().clean()
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Meno'
        self.fields['lastname'].label = 'Priezvisko'
        self.fields['year_of_birth'].label = 'Rok narodenia'
        self.fields['license_validity'].label = 'Platnosť licencie'
        self.fields['player_is_girl'].label = 'Hráč je dievča'
        self.fields['club'].label = 'Klub'

class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = '__all__'

    def clean_club_name(self):
        club_name = self.cleaned_data['club_name']
        duplicity_name = Club.objects.filter(club_name=club_name)
        if duplicity_name.exists():
            validation_error = "Klub s tímto názvem již existuje v databázi"
            raise ValidationError(validation_error)
        else:
            return club_name

    def clean(self):
        result = super().clean()
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club_name'].label = 'Názov klubu'
class SeasonForm(ModelForm):
    class Meta:
        model = Season
        fields = '__all__'

    season_name = CharField(max_length=64)

    def clean_season_name(self):
        season_name = self.cleaned_data['season_name']
        duplicity_name = Season.objects.filter(season_name=season_name)
        if duplicity_name.exists():
            validation_error = "Tato sezóna již existuje v databázi"
            raise ValidationError(validation_error)
        else:
            return season_name

    def clean(self):
        result = super().clean()
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['season_name'].label = 'Sezóna v tvare 2022/2023'

class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = '__all__'

    league_name = CharField(max_length=32)

    def clean_league_name(self):
        league_name = self.cleaned_data['league_name']
        duplicity_name = League.objects.filter(league_name=league_name)
        if duplicity_name.exists():
            validation_error = "Tato liga již existuje v databázi"
            raise ValidationError(validation_error)
        else:
            return league_name

    def clean(self):
        result = super().clean()
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['league_name'].label = 'Liga'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    category_name = CharField(max_length=32)

    def clean_category_name(self):
        category_name = self.cleaned_data['category_name']
        duplicity_name = Category.objects.filter(category_name=category_name)
        if duplicity_name.exists():
            validation_error = "Tato věková kategorie již existuje v databázi"
            raise ValidationError(validation_error)
        else:
            return category_name

    def clean(self):
        result = super().clean()
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category_name'].label = 'Veková kategória'

class DisciplineForm(ModelForm):
    class Meta:
        model = Discipline
        fields = '__all__'

    discipline_name = CharField(max_length=32)

    def clean_discipline_name(self):
        discipline_name = self.cleaned_data['discipline_name']
        duplicity_name = Discipline.objects.filter(discipline_name=discipline_name)
        if duplicity_name.exists():
            validation_error = "Tato disciplína již existuje v databázi"
            raise ValidationError(validation_error)
        else:
            return discipline_name

    def clean(self):
        result = super().clean()
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discipline_name'].label = 'Disciplína'

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
        return organizer_name

    def clean_organizer_lastname(self):
        organizer_lastname = self.cleaned_data['organizer_lastname']
        return organizer_lastname

    def clean(self):
        result = super().clean()
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organizer_name'].label = 'Meno organizátora'
        self.fields['organizer_lastname'].label = 'Priezvisko organizátora'
        self.fields['organizer_mail'].label = 'Email'
        self.fields['organizer_phone'].label = 'Telefónne číslo'

class PropositionForm(ModelForm):
    class Meta:
        model = Propositions
        fields = ['prescription', 'tournament_system', 'notes', 'category', 'league', 'discipline', 'event_location',
                  'event_date', 'schedule', 'season', 'tournament_order', 'organizer_club', 'director', 'judge', 'registration']
        widgets = {
            'event_date': SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prescription'].label = 'Predpis'
        self.fields['prescription'].widget.attrs.update({'rows':'4'})
        self.fields['tournament_system'].label = 'Systém turnaja'
        self.fields['tournament_system'].widget.attrs.update({'rows': '4'})
        self.fields['notes'].label = 'Poznámky'
        self.fields['notes'].widget.attrs.update({'rows': '4'})
        self.fields['category'].label = 'Kategória'
        self.fields['league'].label = 'Liga'
        self.fields['discipline'].label = 'Disciplína'
        self.fields['event_location'].label = 'Miesto'
        self.fields['event_date'].label = 'Dátum usporiadania'
        self.fields['schedule'].label = 'Časový rozpis'
        self.fields['season'].label = 'Sezóna'
        self.fields['tournament_order'].label = 'Poradie turnaja v sezóne'
        self.fields['organizer_club'].label = 'Organizátor'
        self.fields['registration'].label = 'Prihlášky'
        self.fields['director'].label = 'Riaditeľ'
        self.fields['judge'].label = 'Hlavný rozhodca'

    category = ModelMultipleChoiceField(queryset=Category.objects.all())
    league = ModelMultipleChoiceField(queryset=League.objects.all())
    discipline = ModelMultipleChoiceField(queryset=Discipline.objects.all())
    schedule = ModelMultipleChoiceField(queryset=Schedule.objects.all())
    season = ModelChoiceField(queryset=Season.objects.all())


class ResultsAddForm(ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'

    class Meta:
        model = Result
        fields = ['player', 'result']
        exclude = ['tournament']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['player'].label = 'Meno hráča'
        # self.fields['tournament'].label = 'Poradie turnaja v sezóne'
        self.fields['result'].label = 'Body'
        tournament = kwargs.pop('tournament', None)
        super(ResultsAddForm, self).__init__(*args, **kwargs)
        if tournament:
            self.fields['tournament'].initial = tournament


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'description', 'propositions', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Názov'
        self.fields['description'].label = 'Popis'
        self.fields['propositions'].label = 'Propozície'
        self.fields['category'].label = 'Kategória'