from django import forms
from player.models import *


# Anything added to this form needs to be processed on the first step of character creation
# in classes/createPlayer.py
class CreatePlayerPart1Form(forms.Form):
    character_name = forms.CharField(max_length=200, label="Character Name")
    photo = forms.ImageField(max_length=200, label="Character photo")
    gender = forms.ChoiceField(choices=(("Male", "Male"),
                                        ("Female", "Female"),
                                        ("Other", "Other")), label="Gender")
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


class CreateClassForm(forms.Form):
    name = forms.CharField(max_length=100, label="Class Name")
    shorthand = forms.CharField(max_length=3, label="Short hand")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    # image = forms.ImageField(label="image")
    hitDie = forms.CharField(max_length=6, label="Hit Dice")
    alignment = forms.ModelMultipleChoiceField(queryset=Alignment.objects.all(),
                                               label="Allowed Alignments")
    classSkills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                                 label="Class Skills")
    ranks = forms.IntegerField(label="Skill ranks")


class CreateClassLevelForm(forms.Form):
    level = forms.IntegerField(label="Level")
    bab1 = forms.IntegerField(label="Base Attack Bonus 1", initial=0)
    bab2 = forms.IntegerField(label="Base Attack Bonus 2", initial=0)
    bab3 = forms.IntegerField(label="Base Attack Bonus 3", initial=0)
    bab4 = forms.IntegerField(label="Base Attack Bonus 4", initial=0)
    fort = forms.IntegerField(label="Fortitude Save Bonus", initial=0)
    ref = forms.IntegerField(label="Reflex Save Bonus", initial=0)
    will = forms.IntegerField(label="Will Save Bonus", initial=0)
    specialAbilities = forms.ModelMultipleChoiceField(queryset=SpecialAbilities.objects.all(), required=False)