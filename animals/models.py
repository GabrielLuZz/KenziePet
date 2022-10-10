from email.policy import default
from random import choices
from django.db import models
import math


class SexChoices(models.TextChoices):
    MALE = "Macho"
    FEMALE = 'Fêmea'
    DEFAULT = 'Não informado'


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, choices=SexChoices.choices, default=SexChoices.DEFAULT
    )

    group = models.ForeignKey(
        'groups.Group', on_delete=models.CASCADE, related_name='animals'
    )

    traits = models.ManyToManyField('traits.Trait', related_name='animals')

    def convert_dog_age_to_human_years(self):
        return (16 * math.log(self.age)) + 31
