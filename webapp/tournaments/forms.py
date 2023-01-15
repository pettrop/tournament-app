from django.forms import (
    ModelForm, CharField, DateField, IntegerField, ModelChoiceField, ModelMultipleChoiceField, SelectDateWidget)

from tournaments.models import Club, Player, Propositions, Category, League, Discipline, Schedule, Season, Organizer


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
