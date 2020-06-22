from django.db import models


class Abilities(models.Model):
    strength = models.IntegerField
    dexterity = models.IntegerField
    constitution = models.IntegerField
    wisdom = models.IntegerField
    intelligence = models.IntegerField
    charisma = models.IntegerField


class Skill(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    untrained = models.BooleanField
    ability = models.CharField(max_length=3)
    description = models.TextField


class SkillRank(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    ranks = models.IntegerField


class Effect(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
    abilities = models.ForeignKey(Abilities, on_delete=models.SET_NULL, null=True)
    skills = models.ManyToManyField(SkillRank)
    

#TODO: Need to finish ActiveEffect :)
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
    size = models.CharField(max_length=1, choices=super().SIZES, default='M')
    weight = models.IntegerField
    location = models.CharField(max_length=200, blank=True)

    def canBeWorn(self):
        return False
    
    def getWeight(self, quantity=1):
        return self.weight

    def canBeWielded(self):
        return False


# TODO: Finsih Spell Class
class Spell(CommonInfo):
    effect = models.TextField


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
    extraDamage = models.IntegerField
    ammountPerWeight = models.IntegerField
    
    def getWeight(self, quantity=1):
        weight = quantity / self.ammountPerWeight * self.weight
        if quantity % self.ammountPerWeight > self.ammountPerWeight / 2:
            weight += 1
        return weight


class AmmoBundle(WieldableItem):
    ammo = models.ManyToManyField(Ammo)
    quantity = models.IntegerField


class Weapon(WieldableItem):
    blunt = models.BooleanField
    pierce = models.BooleanField
    slash = models.BooleanField
    damage = models.CharField(max_length=9)
    criticalRange = models.IntegerField
    critical = models.IntegerField
    ammo = models.ForeignKey(Ammo)
    ranged = models.BooleanField
    range = models.IntegerField
    hands = models.IntegerField


# TODO: finish Armor Class
class Armor(WearableItem):
    ac = models.IntegerField
    arcaneFailure = models.IntegerField
    maxDex = models.IntegerField
    ACPenalty = models.IntegerField


# TODO: Finish Shield Class
class Shield(Armor):
    WIELDING = {
        ("1H", "One Handed"),
        ("2H", "Two Handed")
    }
    hands = models.CharField(max_length=2, choices=WIELDING, )

    def canBeWielded(self):
        return True


# TODO: Finish Magical Item
class MagicalItem(Item):
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    weight = models.IntegerField


class InventoryItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    knowsSpecialProperties = models.BooleanField
    knowsSpecialName = models.BooleanField

    def getWeight(self, quantity=1):
        self.item.getWeight()


class Equipment(models.Model):
    armor = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    leftHand = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    rightHand = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    carriedEquipment = models.ManyToManyField(InventoryItem, on_delete=models.CASCADE)
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


class Inventory(models.Model):
    items = models.ManyToManyField(InventoryItem)
    equipment = models.OneToOneField(Equipment)

    def equipItem(self, item, area):
        return self.equipment.equipItem(item, area)

    def carryItem(self, item):
        return self.equipment.carryItem(item)
        

class PC(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    inventory = models.OneToOneField(Inventory)
    abilities = models.OneToOneField(Abilities)
    skillRanks = models.ManyToManyField(SkillRank)
    photo = models.ImageField
    activeEffects = models.ManyToManyField(ActiveEffect)
    maxWeight = models.IntegerField

    def equipItem(self, item, area):
        if self.maxWeight < item.getWeight()+self.maxWeight:
            return "Item is to heavy to be equipped"
        elif item.canBeWielded() or item.canBeWorn():
            return self.inventory.equipItem(item, area)
        else:
            return "Item cannot be equipped"

    def carryItem(self, item):
        if self.maxWeight < item.getWeight()+self.maxWeight:
            return self.inventory.carryItem()

    def getStrength(self):
        return self.abilities.strength
