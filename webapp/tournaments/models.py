from django.db import models

# Create your models here.

## nikde nedavam id / django je vytvori automaticky jako primary key
# nejsou zde spojovaci tabulky - tournament_schedule, tournament_discipline, tournament_organizer, tournament_category
# club_result_tournament a player_resount_tournament nejsou v modelech - to myslím, že uděláme jako funkce do forms.py?
class Tournament(Model):
    name = models.CharField(max_lenght=200, unique=True)
    description = models.TextField(null=True, blank=True)
    # season cizi klic z tabulky season pres id
    # leage cizi klic z tabulky league pres id
    # category cizi klic z tabulky category pres id
    # event_location cizi klic z tabulky event_location pres id
    # event_date cizi klic z tabulky event_date pres id
    # tournament_order poradi ??? z ceho se bere - to bude muset být asi funkce ve forms?
    # proposition cizi klic pres id - nebo proklik v vypsani proposic zadavanych v tabulce proposition
    created = models.DataTimeField(auto_now_add=True)
    updated = models.DataTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', 'name']

class Proposition(Models):
    # email cizi klic tabulky email pres id
    # tel_number cizi klic tabulky tel_number pres id
    start_fee = models.IntegerField(null=False, unique=False) #unique tady asi ani nemusi byt
    prescription = models.CharField(max_lenght=400)
    tournament_system = models.CharField(max_lenght=400)
    notes = models.CharField(max_lenght=400)

    # def __str__(self): nevím na co tuto metodu přetížit
    #     return self.

    class Meta:
        ordering = ['-created']

class Organizer(Models): #zvažit zda se neda zahrnout do tabulky Proposition
    organizer_name = models.CharField(max_lenght=100)
    # function cizi klic tabulky function pres id

    def __str__(self):
        return self.organizer_name

class Function(Models): #zvažit zda se neda zahrnout do tabulky Proposiotin společně s Organizer - napřiklad jako dvě hodnoty organizator turnaje, ředitel turnaje
    function_name = models.CharField(max_lenght=100)

    def __str__(self):
        return self.function_name


# zvážit, zda tabulku schedule nezahrnout do Proposition jako:
# registration time, start time, end time, pripadne ještě description, ale v Proposition už je prescription, to by mohlo obsáhnout oboje.
# zvážit, zda tabulky season, league, category, event_location a event_date nezahrnout také do Proposition.

class Discipline(Models):
    name = name = models.CharField(max_lenght=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']



class Player(Model):
    reg_number = models.IntegerField(null=False, unique=True)
    name = models.CharField(max_lenght=200)
    lastname = models.CharField(max_lenght=200)
    year_of_birth = models.IntegerField(null=False, unique=True) # nevim, zda u DataTimeField jde zadat jen rok
    licence_validity = models.DataTimeField(null=False, unique=True) #auto false?
    # club cizi klic z tabulky club pres id

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = [???]

class Club(Models):
    name = models.CharField(max_lenght=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']