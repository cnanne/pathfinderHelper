from django.db import models
from player.classes.commonInfo import CommonInfo


# TODO: Finsih Spell Class
class Spell(CommonInfo):
    effect = models.TextField()

    def __str__(self):
        return self.name