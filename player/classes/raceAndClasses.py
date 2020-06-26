from django.db import models
from player.classes.items import *


class Class(CommonInfo):
    shortHand = models.CharField(max_length=3)
    hitDie = models.CharField(max_length=6)
    alignment = models.ManyToManyField(Alignment)
    classSkills = models.ManyToManyField(Skill, blank=True)
    ranks = models.IntegerField()


class ClassLevel(models.Model):
    gameClass = models.ForeignKey(Class, on_delete=models.CASCADE)
    level = models.IntegerField()
    bab1 = models.IntegerField()
    bab2 = models.IntegerField()
    bab3 = models.IntegerField()
    bab4 = models.IntegerField()
    fort = models.IntegerField()
    ref = models.IntegerField()
    will = models.IntegerField()
    specialAbilities = models.ManyToManyField(SpecialAbilities, blank=True)

    def getLevel(self):
        return self.gameClass.shortHand + "/" + self.level.__str__()


class Race(CommonInfo):
    abilities = models.ForeignKey(Abilities, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=CommonInfo.SIZES)
    raceSpecialAbilities = models.ManyToManyField(SpecialAbilities, blank=True)
    speed = models.IntegerField(default=30)
    fort = models.IntegerField(default=0)
    will = models.IntegerField(default=0)
    ref = models.IntegerField(default=0)


class SelectedRace(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    appliedAbilities = models.ForeignKey(Abilities, on_delete=models.CASCADE)