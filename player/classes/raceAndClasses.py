from django.db import models
from player.classes.items import *
from player.classes.alignment import *
from player.classes.specialAbilities import *



class Language(models.Model):
    name = models.CharField(max_length=100)


class Class(CommonInfo):
    shortHand = models.CharField(max_length=3)
    hitDie = models.CharField(max_length=6)
    hp = models.IntegerField(default=0)
    alignment = models.ManyToManyField(Alignment)
    classSkills = models.ManyToManyField(Skill, blank=True)
    ranks = models.IntegerField()

    def __str__(self):
        return self.name


class ClassLevel(models.Model):
    name = models.CharField(max_length=10, primary_key=True, blank=True)
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

    def __str__(self):
        return self.gameClass.shortHand + str(self.level)

    def getLevel(self, level):
        return ClassLevel.objects.get(name=self.gameClass.shortHand+str(level))

    def getNextLevel(self):
        return self.getLevel(self.level+1)

    def getPrevLevel(self):
        if self.level - 1 <= 0:
            return self
        return self.getLevel(self.level-1)

    def save(self, *args, **kwargs):
        self.name = self.gameClass.shortHand + str(self.level)
        super().save(*args, **kwargs)


# TODO: Need to add Language
class Race(CommonInfo):
    abilities = models.ForeignKey(Abilities, on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language, blank=True)
    size = models.CharField(max_length=1, choices=CommonInfo.SIZES)
    raceSpecialAbilities = models.ManyToManyField(SpecialAbilities, blank=True)
    speed = models.IntegerField(default=30)
    fort = models.IntegerField(default=0)
    will = models.IntegerField(default=0)
    ref = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SelectedRace(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    appliedAbilities = models.ForeignKey(Abilities, on_delete=models.CASCADE)