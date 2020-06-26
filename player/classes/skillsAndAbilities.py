from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    subclass = models.CharField(max_length=100, default="", blank=True)
    acPenalty = models.BooleanField(default=False)
    untrained = models.BooleanField()
    ability = models.CharField(max_length=3)
    description = models.TextField()
    url = models.URLField()

    def fillData(self, name, untrained, ability, description):
        self.name = name
        self.untrained = untrained
        self.ability = ability
        self.description = description


class SkillRank(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    ranks = models.IntegerField()

    @classmethod
    def create(cls, skill, ranks):
        skillRank = cls(skill=skill, ranks=ranks)
        return skillRank


class Abilities(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    strength = models.IntegerField(default=0)
    dexterity = models.IntegerField(default=0)
    constitution = models.IntegerField(default=0)
    wisdom = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    charisma = models.IntegerField(default=0)

    def __add__(self, other):
        self.strength += other.strength
        self.dexterity += other.dexterity
        self.constitution += other.constitution
        self.wisdom += other.wisdom
        self.intelligence += other.intelligence
        self.charisma += other.charisma
        return self


class AbilitiesMap():
    str = dex = con = wis = int = cha = 10
    strMod = dexMod = conMod = wisMod = intMod = chaMod = 0

    def __init__(self, abilitiesDict):
        self.str = abilitiesDict["STR"]["score"]
        self.strMod = abilitiesDict["STR"]["mod"]
        self.dex = abilitiesDict["DEX"]["score"]
        self.dexMod = abilitiesDict["DEX"]["mod"]
        self.con = abilitiesDict["CON"]["score"]
        self.conMod = abilitiesDict["CON"]["mod"]
        self.wis = abilitiesDict["WIS"]["score"]
        self.wisMod = abilitiesDict["WIS"]["mod"]
        self.int = abilitiesDict["INT"]["score"]
        self.intMod = abilitiesDict["INT"]["mod"]
        self.cha = abilitiesDict["CHA"]["score"]
        self.chaMod = abilitiesDict["CHA"]["mod"]
