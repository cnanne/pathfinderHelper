from django.db import models
from player.classes.items import *


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