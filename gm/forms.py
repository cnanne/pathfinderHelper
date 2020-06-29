from django import forms
from player.models import *


class CreatePlayerPart1(forms.Form):
    character_name = forms.CharField(max_length=200, label="Character Name")
    photo = forms.ImageField(max_length=200, label="Character photo")
    str = forms.IntegerField(label="Strength")
    dex = forms.IntegerField(label="Dexterity")
    con = forms.IntegerField(label="Constitutions")
    wis = forms.IntegerField(label="Wisdom")
    int = forms.IntegerField(label="Intelligence")
    cha = forms.IntegerField(label="Charisma")
    race = forms.ModelChoiceField(queryset=Race.objects.all(),
                                  label="Race")
