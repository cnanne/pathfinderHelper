from django.db import models


class CommonInfo(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(null=True)

    SIZES = [
        ('F', 'Fine'),
        ('D', 'Diminutive'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('H', 'Huge'),
        ('G', 'Gargantuan'),
        ('C', 'Colossal')
    ]

    class Meta:
        abstract = True