from django.core.exceptions import ValidationError
from django.forms import (
    Form, Textarea, ModelForm, CharField, DateField, IntegerField, ModelChoiceField)
from django.template import defaulttags

from tournaments.models import Club, Player, Season, League, Category


# class PlayerForm(Form):
#     name = CharField(max_length=32)
#     lastname = CharField(max_length=32)
#     year_of_birth = IntegerField()
#     license_validity = DateField()

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

    league_name = CharField(max_length=32) # odstranila jsem unique=True / TypeError: __init__() got an unexpected keyword argument 'unique'

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

    category_name = CharField(max_length=32) # odstranila jsem unique=True / TypeError: __init__() got an unexpected keyword argument 'unique'

    def clean_category_name(self):
            category_name = self.cleaned_data['category_name']
            return category_name.capitalize()

    def clean(self):
            result = super().clean()
            return result