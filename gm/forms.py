from django import forms
from player.models import *


# Anything added to this form needs to be processed on the first step of character creation
# in classes/createPlayer.py
class CreatePlayerPart1Form(forms.Form):
    character_name = forms.CharField(max_length=200, label="Character Name")
    photo = forms.ImageField(max_length=200, label="Character photo")
    gender = forms.ChoiceField(choices=("Male",
                                        "Female",
                                        "Other"), label="Gender")
    str = forms.IntegerField(label="Strength", initial=10)
    dex = forms.IntegerField(label="Dexterity", initial=10)
    con = forms.IntegerField(label="Constitutions", initial=10)
    wis = forms.IntegerField(label="Wisdom", initial=10)
    int = forms.IntegerField(label="Intelligence", initial=10)
    cha = forms.IntegerField(label="Charisma", initial=10)
    race = forms.ModelChoiceField(queryset=Race.objects.all(),
                                  label="Race")
    alignment = forms.ModelChoiceField(queryset=Alignment.objects.all(),
                                       label="Alignment")
    height = forms.IntegerField(label="Height")
    age = forms.IntegerField(label="Age")
    weight = forms.IntegerField(label="Weight")
    eyes = forms.CharField(label="Eye Color", max_length=100)
    hair = forms.CharField(label="Hair Color", max_length=100)