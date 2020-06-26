from django.db import models
from player.classes.items import *


# TODO: Finsih Spell Class
class Spell(CommonInfo):
    effect = models.TextField()