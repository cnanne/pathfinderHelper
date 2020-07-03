from django.db import models
from player.classes.items import *


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)

    def __iadd__(self, other):
        for item in other.items.all():
            item.inventory = self
        return self

    def getWeight(self):
        weight = 0
        for item in self.items.all():
            weight += item.getWeight()
        return weight

    def __str__(self):
        return "Inventory @ " + self.location.name


class InventoryItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="items")
    knowsSpecialProperties = models.BooleanField()
    knowsSpecialName = models.BooleanField()

    def getWeight(self, quantity=1):
        return self.item.getWeight() * quantity

    def moveItem(self, inventory):
        self.inventory = inventory

    def __str__(self):
        return self.item.__str__() + " @ " + self.inventory.location.__str__()


class Equipment(models.Model):
    armor = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, blank=True, null=True, related_name='armors')
    leftHand = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='leftHanded')
    rightHand = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='righthanded')
    primaryHand = models.CharField(max_length=1, default="R")
    eyes = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, blank=True, null=True, related_name="eyes")
    legs = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, blank=True, null=True, related_name="legs")
    neck = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, blank=True, null=True, related_name="neck")
    feet = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, blank=True, null=True, related_name="feet")

    def __str__(self):
        return self.pc.name + '\'s equipment'

    def weightOfOtherEquipment(self):
        weight = 0
        weight = self.eyes.getWeight() + self.legs.getWeight() + self.neck.getWeight()
        return 0

    def getWeight(self):
        weight = self.carriedEquipment.getWeight()
        weight += (self.armor.getWeight() + self.leftHand.getWeight() + self.weightOfOtherEquipment())
        return weight

    def equipItem(self, item, area):
        if not item.canBeEquipped():
            return
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
        if self.rightHand is not None:
            self.carryItem(self.rightHand)
        self.rightHand(item)

    def equipArmor(self, item):
        if not item.canBeWorn():
            return
        wearable = WearableItem(item)
        if wearable.area == "TORSO":
            if self.armor is not None:
                self.armor.inventory = self.carriedEquipment
            self.armor = item

    def equipBH(self, item):
        if self.primaryHand == "RH":
            self.equipRH(item)
        else:
            self.equipLH(item)

    def carryItem(self, item):
        InventoryItem(item).inventory = self.carriedEquipment
