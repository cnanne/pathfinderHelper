from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    subclass = models.CharField(max_length=100, blank=True)
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

    def __str__(self):
        name = self.name
        if self.subclass is not None:
            name += (" (" + self.subclass + ")")
        return self.name


class SkillRank(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    ranks = models.IntegerField()

    @classmethod
    def create(cls, skill, ranks):
        skillRank = cls(skill=skill, ranks=ranks)
        return skillRank

    def addRank(self):
        self.ranks += 1

    @property
    def totalRanks(self):
        return self.ranks


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

    def __str__(self):
        return self.name

    @staticmethod
    def makeAbilityDictionary(abilityScore):
        return {"score": abilityScore, "mod": Abilities.calculateModifier(abilityScore)}

    @staticmethod
    def calculateModifier(ability):
        mod = 0
        if ability >= 10:
            mod = int((ability - 10) / 2)
        else:
            mod = int((ability - 10) / 2) - 1
        return mod

    def makeDictionary(self):
        abilities = {"STR": self.makeAbilityDictionary(self.strength),
                     "DEX": self.makeAbilityDictionary(self.dexterity),
                     "CON": self.makeAbilityDictionary(self.constitution),
                     "WIS": self.makeAbilityDictionary(self.wisdom),
                     "INT": self.makeAbilityDictionary(self.intelligence),
                     "CHA": self.makeAbilityDictionary(self.charisma)}
        return abilities



class AbilitiesMap:
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
