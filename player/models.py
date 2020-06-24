from django.db import models


class Abilities(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    wisdom = models.IntegerField()
    intelligence = models.IntegerField()
    charisma = models.IntegerField()

    def __add__(self, other):
        self.strength += other.strength
        self.dexterity += other.dexterity
        self.constitution += other.consitution
        self.wisdom += other.wisdom
        self.intelligence += other.intelligence
        self.charisma += other.charisma


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


class Effect(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
    abilities = models.ForeignKey(Abilities, on_delete=models.SET_NULL, null=True)
    attackBonus = models.IntegerField(default=0)
    extraDamage = models.IntegerField(default=0)
    damage = models.CharField(max_length=10)


class EffectSkillRank(SkillRank):
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)


# TODO: Need to finish ActiveEffect :)
class ActiveEffect(models.Model):
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)


class CommonInfo(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(null=True)

    SIZES = [
        ('F', 'Fine'),
        ('D', 'Diminutive'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('H', 'Huge'),
        ('G', 'Gargantuan'),
        ('C', 'Colossal')
    ]

    class Meta:
        abstract = True


class Item(CommonInfo):
    specialProperties = models.TextField(blank=True)
    specialName = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=1, choices=CommonInfo.SIZES, default='M')
    weight = models.IntegerField()
    masterwork = models.BooleanField()
    effects = models.ForeignKey(Effect, on_delete=models.SET_NULL, null=True)
    material = models.CharField(max_length=100, default="Normal")

    def canBeWorn(self):
        return False

    def getWeight(self, quantity=1):
        return self.weight

    def canBeWielded(self):
        return False


# TODO: Finsih Spell Class
class Spell(CommonInfo):
    effect = models.TextField()


class WearableItem(Item):
    area = models.CharField(max_length=50)

    def canBeWorn(self):
        return True


class WieldableItem(Item):
    WIELDING = {
        ("1H", "One Handed"),
        ("2H", "Two Handed")
    }
    area = models.CharField(max_length=2, choices=WIELDING)

    def canBeWielded(self):
        return True


class Ammo(Item):
    damage = models.CharField(max_length=10)
    extraDamage = models.IntegerField()
    ammountPerWeight = models.IntegerField()

    def getWeight(self, quantity=1):
        weight = quantity / self.ammountPerWeight * self.weight
        if quantity % self.ammountPerWeight > self.ammountPerWeight / 2:
            weight += 1
        return weight


class AmmoBundle(WieldableItem):
    ammo = models.ManyToManyField(Ammo)
    quantity = models.IntegerField()


class Weapon(WieldableItem):
    blunt = models.BooleanField(default=False)
    pierce = models.BooleanField(default=False)
    slash = models.BooleanField(default=False)
    damage = models.CharField(max_length=9)
    criticalRange = models.IntegerField()
    critical = models.IntegerField()
    defualtAmmo = models.ForeignKey(Ammo, on_delete=models.SET_NULL, null=True)
    ranged = models.BooleanField()
    range = models.IntegerField()
    hands = models.IntegerField()


# TODO: finish Armor Class
class Armor(WearableItem):
    ac = models.IntegerField()
    arcaneFailure = models.IntegerField()
    maxDex = models.IntegerField()
    ACPenalty = models.IntegerField()


# TODO: Finish Shield Class
class Shield(Armor):
    WIELDING = {
        ("1H", "One Handed")
    }
    hands = models.CharField(max_length=2, choices=WIELDING)

    def canBeWielded(self):
        return True


# TODO: Finish Magical Item
class MagicalItem(Item):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)


class Location(models.Model):
    name = models.CharField(max_length=100)


class Inventory(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class InventoryItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    knowsSpecialProperties = models.BooleanField()
    knowsSpecialName = models.BooleanField()

    def getWeight(self, quantity=1):
        return self.item.getWeight() * quantity


class Equipment(models.Model):
    armor = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, blank=True, null=True, related_name='armors')
    leftHand = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='leftHanded')
    rightHand = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='righthanded')
    carriedEquipment = models.ManyToManyField(InventoryItem, blank=True)
    primaryHand = models.CharField(max_length=1, default="R")

    def equipItem(self, item, area):
        if area == "LH":
            self.equipLH(item)
        elif area == "RH":
            self.equipRH(item)
        elif area == "Torso":
            self.equipArmor(item)
        elif area == "BH":
            self.equipBH(item)
        return None

    def equipLH(self, item):
        pass

    def equipRH(self, item):
        pass

    def equipArmor(self, item):
        pass

    def equipBH(self, item):
        pass

    def carryItem(self, item):
        pass


class SpecialAbilities(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Alignment(models.Model):
    ALIGNMENTS = {
        ("CE", "Chaotic Evil"),
        ("NE", "Neutral Evil"),
        ("LE", "Lawful Evil"),
        ("CN", "Chaotic Neutral"),
        ("NN", "True Neutral"),
        ("LN", "Lawful Neutral"),
        ("CG", "Chaotic Good"),
        ("NG", "Neutral Good"),
        ("LG", "Lawful Good")

    }
    name = models.CharField(max_length=100)
    alignment = models.CharField(max_length=2, choices=ALIGNMENTS)


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
    specialAbilities = models.ManyToManyField(SpecialAbilities, blank=True, null=True)

    def getLevel(self):
        return self.gameClass.shortHand + "/" + self.level.__str__()


class Race(CommonInfo):
    abilities = models.ForeignKey(Abilities, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=CommonInfo.SIZES)
    raceSpecialAbilities = models.ManyToManyField(SpecialAbilities, blank=True)
    speed = models.IntegerField(default=30)


class SelectedRace(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    appliedAbilities = models.ForeignKey(Abilities, on_delete=models.CASCADE)

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


class PC(models.Model):
    playerName = models.CharField(max_length=200)
    name = models.CharField(max_length=200, primary_key=True)
    race = models.OneToOneField(SelectedRace, on_delete=models.CASCADE, blank=True, null=True)
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank=True)
    abilities = models.OneToOneField(Abilities, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, null=True)
    activeEffects = models.ManyToManyField(ActiveEffect, blank=True)
    alignment = models.ForeignKey(Alignment, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=50, default="Male")
    classLevels = models.ManyToManyField(ClassLevel, blank=True)

    def maxWeight(self):
        return 0

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
            level = level + classLevel.getLevel()
            if not first:
                level = level + "-"
            first = False
        return level

    def getBab(self):
        classLevels = self.classLevels
        bab = [0, 0, 0, 0]
        for classLevel in classLevels.all():
            bab[0] += classLevel.bab1
            bab[1] += classLevel.bab2
            bab[2] += classLevel.bab3
            bab[3] += classLevel.bab4
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
        skillRanks = self.pcskillrank_set.all()
        abilities = self.getAbilitiesSocresAndModifiers()
        classSkills = self.getClassSkills()
        for skill in skillRanks:
            name = skill.skill.name
            ranks = skill.ranks
            ranks += abilities[skill.skill.ability]
            if skill.skill.name in classSkills:
                ranks += 3
            skills[name] = ranks
        for effect in self.activeEffects.all():
            for skillRank in effect.effectskillrank_set.all():
                if skillRank.skill.name not in skills:
                    skills[skillRank.skill.name] = skillRank.ranks
                else:
                    skills[skillRank.skill.name] += skillRank.ranks

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
        pass


class PCSkillRank(SkillRank):
    pc = models.ForeignKey(PC, on_delete=models.CASCADE)
