from django.db import models
from player.classes.skillsAndAbilities import *
from player.classes.effects import *
from player.classes.items import *
from player.classes.spells import *
from player.classes.inventoryAndEquipment import *
from player.classes.raceAndClasses import *


class Saves:
    fort = dex = will = 0

    def __init__(self, saves):
        self.fort = saves["fort"]
        self.will = saves["will"]
        self.ref = saves["ref"]


class PC(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    race = models.OneToOneField(SelectedRace, on_delete=models.CASCADE, blank=True, null=True)
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank=True)
    abilities = models.ForeignKey(Abilities, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="images/",blank=True, null=True)
    activeEffects = models.ManyToManyField(ActiveEffect, blank=True)
    alignment = models.ForeignKey(Alignment, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=50, default="Male")
    classLevels = models.ManyToManyField(PlayerClassLevel, blank=True)
    weight = models.IntegerField(blank=True, default=0, null=True)
    age = models.IntegerField(blank=True, default=0, null=True)
    hair = models.CharField(max_length=100, blank=True, default="Blonde", null=True)
    eyes = models.CharField(max_length=100, blank=True, default="Green", null=True)

    def __str__(self):
        return self.name

    # TODO: need to implement
    def maxWeight(self):
        pass

    def equipItem(self, item, area):
        if self.maxWeight < item.getWeight() + self.maxWeight:
            return "Item is to heavy to be equipped"
        elif item.canBeWielded() or item.canBeWorn():
            return self.equipment.equipItem(item, area)
        else:
            return "Item cannot be equipped"

    def carryItem(self, item):
        if self.maxWeight < item.getWeight() + self.maxWeight:
            return "Item is to heavy to carry"
        else:
            return self.equipment.carryItem(item)

    def getStrength(self):
        return self.abilities.strength

    def getAlignment(self):
        return self.alignment.alignment

    def getLevels(self):
        classLevels = self.classLevels
        first = True
        level = ""
        for classLevel in classLevels.all():
            if not first:
                level = level + "-"
            level = level + classLevel.getLevel()
            first = False
        return level

    def getBab(self):
        classLevels = self.classLevels
        bab = [0, 0, 0, 0]
        for classLevel in classLevels.all():
            bab[0] += classLevel.classLevel.bab1
            bab[1] += classLevel.classLevel.bab2
            bab[2] += classLevel.classLevel.bab3
            bab[3] += classLevel.classLevel.bab4
        activeEffectsAttack = 0
        activeEffectsAttack += self.activeEffectsAttackBonus()
        bab[0] += activeEffectsAttack
        if bab[1] > 0:
            bab[1] += activeEffectsAttack
        if bab[2] > 0:
            bab[2] += activeEffectsAttack
        if bab[3] > 0:
            bab[3] += activeEffectsAttack
        return bab

    def getSize(self):
        return self.race.race.size

    def getRaceName(self):
        return self.race.race.name

    def getSpeed(self):
        return self.race.race.speed

    def activeEffectsAttackBonus(self):
        activeEffects = self.activeEffects
        attack = 0
        for activeEffect in activeEffects.all():
            attack += activeEffect.attackBonus
        return attack

    def getSkills(self):
        skills = {}
        skillRanks = self.skillRanks.all()
        abilities = self.getAbilitiesSocresAndModifiers
        classSkills = self.getClassSkills()
        for skill in skillRanks:
            name = skill.skill.name
            ranks = skill.ranks
            ranks += abilities[skill.skill.ability]["mod"]
            for classSkill in classSkills:
                if skill.skill.name == classSkill.name:
                    ranks += 3
                    break
            skills[name] = SkillRank.create(skill.skill,
                                            ranks)
        for effect in self.activeEffects.all():
            for skillRank in effect.effectskillrank_set.all():
                if skillRank.skill.name in skills.keys():
                    skills[skillRank.skill.name].ranks += skillRank.ranks
                else:
                    skill = SkillRank()
                    skill.skill = skillRank.skill
                    skill.ranks = skillRank.ranks
                    skills[skillRank.skill.name] = skill
        return skills

    @property
    def getAbilitiesMap(self):
        return self.getAbilitiesSocresAndModifiers

    @property
    def getAbilitiesSocresAndModifiers(self):
        abilities = self.getAbilities()
        return {"STR": self.makeAbilitydictionary(abilities.strength),
                "DEX": self.makeAbilitydictionary(abilities.dexterity),
                "CON": self.makeAbilitydictionary(abilities.constitution),
                "WIS": self.makeAbilitydictionary(abilities.wisdom),
                "INT": self.makeAbilitydictionary(abilities.intelligence),
                "CHA": self.makeAbilitydictionary(abilities.charisma)}

    def makeAbilitydictionary(self, abilityScore):
        return {"score": abilityScore, "mod": self.calculateModifier(abilityScore)}

    def getAbilities(self):
        abilities = Abilities()
        abilities += self.abilities
        for effect in self.activeEffects.all():
            abilities += effect.abilities
        return abilities

    def calculateModifier(self, ability):
        mod = 0
        if ability >= 10:
            mod = int((ability - 10) / 2)
        else:
            mod = int((ability - 10) / 2) - 1
        return mod

    def getClassSkills(self):
        classLevels = self.classLevels
        classSkills = []
        for classLevel in classLevels.all():
            skills = classLevel.gameClass.classSkills
            for skill in skills.all():
                if skill.name not in classSkills:
                    classSkills.append(skill)
        return classSkills

    def getSaves(self):
        ref = 0
        fort = 0
        will = 0
        classes = self.classLevels.all()
        for classLevel in classes:
            ref = ref + classLevel.ref
            fort += classLevel.fort
            will += classLevel.will
        activeEffects = self.activeEffects.all()
        for activeEffect in activeEffects:
            ref = activeEffect.effect.ref
            fort = activeEffect.effect.fort
            will = activeEffect.effect.will
        ref += self.race.race.ref
        will += self.race.race.will
        fort += self.race.race.fort
        saves = Saves({"ref": ref, "will": will, "fort": fort})
        return saves

    def getAttacks(self):
        bab = self.getBab()
        rh = self.equipment.rightHand
        lh = self.equipment.leftHand

    def availableClassesForNewLevel(self):
        levels = []
        if self.classLevels.count() == 0:
            classes = Class.objects.all()
            for gameClass in classes:
                classLevel: Class = gameClass
                classLevel = classLevel.classlevel_set.first()
                classLevel = classLevel.getLevel(1)
                levels.append(classLevel)
        else:
            for classLevel in self.classLevels:
                levels.append(classLevel.getNextLevel())
            for gameClass in Class.objects.all():
                for level in levels:
                    if ClassLevel(level).gameClass.name == gameClass.name:
                        continue
                    classLevel = gameClass.objects.first()
                    classLevel = classLevel.getLevel(1)
                    levels.append(classLevel)
        return levels

    def getClassSkills(self):
        classSkills = []
        for playerClassLevel in self.classLevels:
            for skill in playerClassLevel.classLevel.gameClass.classSkills.all():
                if skill.name not in classSkills:
                    classSkills.append(skill.name)
        return classSkills

    def addLevel(self, classLevel, hp):
        pass


class PCSkillRank(SkillRank):
    pc = models.ForeignKey(PC, on_delete=models.CASCADE, related_name="skillRanks")

    def __str__(self):
        return self.pc.name + "'s " + self.skill.name
