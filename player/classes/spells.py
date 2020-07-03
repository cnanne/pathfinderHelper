from django.db import models
from player.classes.commonInfo import CommonInfo


class SpellLevel(models.Model):
    choices = {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)}
    cleric = models.BooleanField(default=None, blank=True, choices=choices)
    paladin = models.IntegerField(default=None, blank=True, choices=choices)
    ranger = models.IntegerField(default=None, blank=True, choices=choices)
    wizardSorcerer = models.IntegerField(default=None, blank=True, choices=choices)
    bard = models.IntegerField(default=None, blank=True, choices=choices)
    druid = models.IntegerField(default=None, blank=True, choices=choices)


class SpellComponents(models.Model):
    components = models.CharField(max_length=10)
    verbal = models.BooleanField(default=False)
    somatic = models.BooleanField(default=False)
    material = models.BooleanField(default=False)
    focus = models.BooleanField(default=False)
    divineFocus = models.BooleanField(default=False)


# TODO: Finsih Spell Class
class Spell(CommonInfo):
    effect = models.TextField()
    spellLevel = models.OneToOneField(SpellLevel, on_delete=models.CASCADE, default=None, null=True)
    castTime = models.IntegerField(default=0)
    school = models.CharField(max_length=100, default="", blank=True)
    target = models.CharField(max_length=100, default="", blank=True)
    components = models.ForeignKey(SpellComponents, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
