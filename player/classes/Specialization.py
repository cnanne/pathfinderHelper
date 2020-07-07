from django.db import models
from player.classes.commonInfo import CommonInfo
from player.classes.raceAndClasses import Class
from player.classes.spells import *


class Specialization(CommonInfo):
    gameClass = models.ForeignKey(Class, on_delete=models.CASCADE)
    @staticmethod
    def isDomain(self):
        return False

    @staticmethod
    def isBloodline(self):
        return False

    @staticmethod
    def isSchool(self):
        return False

    def getSpells(self):
        pass

    def getKnownSpells(self):
        pass

    class Meta:
        abstract = True


class School(Specialization):

    def isSchool(self):
        return True


class Domain(Specialization):
    power1 = models.ForeignKey(Spell, on_delete=models.CASCADE)
    power2 = models.ForeignKey(Spell, on_delete=models.CASCADE)

    def isDomain(self):
        return True

    def getSpells(self):
        return {self.power1.name: self.power1,
                self.power2.name: self.power2}

    def getKnownSpells(self):
        knownSpells = {}
        for domainSpell in self.domainSpells.all():
            knownSpells[domainSpell.name] = domainSpell


class Bloodline(Specialization):

    def isBloodline(self):
        return True

class DomainSpell(Spell):
    domainSpellLevel = models.OneToOneField(SpellLevel)
    domain = models.ForeignKey(Domain, related_name="domainSpells", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def getSpellLevel(self):
        return self.domainSpellLevel

    def isDomainSpell(self):
        return True