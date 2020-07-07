from django.db import models
from player.classes.commonInfo import CommonInfo
from player.classes.raceAndClasses import Class



class SpellLevel(models.Model):
    choices = {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)}
    cleric = models.BooleanField(default=None, blank=True, choices=choices)
    paladin = models.IntegerField(default=None, blank=True, choices=choices)
    ranger = models.IntegerField(default=None, blank=True, choices=choices)
    wizardSorcerer = models.IntegerField(default=None, blank=True, choices=choices)
    bard = models.IntegerField(default=None, blank=True, choices=choices)
    druid = models.IntegerField(default=None, blank=True, choices=choices)
    classes = models.ManyToManyField(Class, default=None, blank=True)

    # when save, assign classes dynamically
    def save(self, *args, **kwargs):
        for gameClass in Class.objects.all():
            if gameClass.name == "Cleric" and self.cleric is not None:
                self.classes.add(gameClass)
            elif gameClass.name == "Paladin" and self.paladin is not None:
                self.classes.add(gameClass)
            elif gameClass.name == "Ranger" and self.ranger is not None:
                self.classes.add(gameClass)
            elif gameClass.name == "Wizard" and self.wizardSorcerer is not None:
                self.classes.add(gameClass)
            elif gameClass.name == "Sorcerer" and self.wizardSorcerer is not None:
                self.classes.add(gameClass)
            elif gameClass.name == "Bard" and self.bard is not None:
                self.classes.add(gameClass)
            elif gameClass.name == "Druid" and self.druid is not None:
                self.classes.add(gameClass)
        super().save(*args, **kwargs)


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

    def getSpellLevel(self):
        return self.spellLevel

    @staticmethod
    def isDomainSpell(self):
        return False




