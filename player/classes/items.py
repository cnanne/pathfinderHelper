from django.db import models
from player.classes.effects import *
from player.classes.spells import *


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