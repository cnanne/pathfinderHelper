
from django.db.models.signals import pre_save
from django.dispatch import receiver
from player.models import *


@receiver(pre_save, sender=PC)
def pre_save(sender, **kwargs):
    PC(sender).createRanks
