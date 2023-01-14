from django.core.exceptions import ValidationError
from django.forms import (
    Form, Textarea, ModelForm, CharField, DateField, IntegerField, ModelChoiceField)
from django.template import defaulttags

from tournaments.models import Club, Player

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