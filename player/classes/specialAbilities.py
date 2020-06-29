from django.db import models

# TODO:Finish this shit.  Missing a lot of shit but basically effects...
class SpecialAbilities(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
