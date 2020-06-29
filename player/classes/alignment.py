from django.db import models


class Alignment(models.Model):
    ALIGNMENTS = {
        ("CE", "Chaotic Evil"),
        ("NE", "Neutral Evil"),
        ("LE", "Lawful Evil"),
        ("CN", "Chaotic Neutral"),
        ("NN", "True Neutral"),
        ("LN", "Lawful Neutral"),
        ("CG", "Chaotic Good"),
        ("NG", "Neutral Good"),
        ("LG", "Lawful Good")

    }
    name = models.CharField(max_length=100)
    alignment = models.CharField(max_length=2, choices=ALIGNMENTS)

    def __str__(self):
        return self.name