from django.db import models
from player.classes.skillsAndAbilities import *


class Effect(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
    abilities = models.ForeignKey(Abilities, on_delete=models.SET_NULL, null=True)
    attackBonus = models.IntegerField(default=0)
    extraDamage = models.IntegerField(default=0)
    damage = models.CharField(max_length=10)
    fort = models.IntegerField(default=0)
    will = models.IntegerField(default=0)
    ref = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class EffectSkillRank(SkillRank):
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)

    def __str__(self):
        effectName = self.effect.name
        skillName = self.skill.name
        return effectName + "_" + skillName


# TODO: Need to finish ActiveEffect :)
class ActiveEffect(models.Model):
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)

    def __str__(self):
        return self.effect.name