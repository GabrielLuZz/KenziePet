from functools import partial
from tokenize import group
from rest_framework import serializers
from traitlets import Instance

from animals.models import Animal, SexChoices
from groups.models import Group
from groups.serializers import GroupSerializer
from traits.models import Trait
from traits.serializers import TraitSerializer

import ipdb


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexChoices.choices,
        default=SexChoices.DEFAULT
    )
    age_in_human_years = serializers.SerializerMethodField()

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, obj):
        return obj.convert_dog_age_to_human_years()

    def create(self, validated_data: dict) -> Animal:
        group = validated_data.pop('group')
        traits = validated_data.pop('traits')

        searched_by_name = Group.objects.filter(name=group['name'])
        searched_by_scientific_name = Group.objects.filter(
            scientific_name=group['scientific_name']
        )

        if searched_by_name and searched_by_scientific_name:
            print('entrei aqui')
            validated_data['group'] = searched_by_name[0]

        if not searched_by_name and not searched_by_scientific_name:
            validated_data['group'] = Group.objects.create(**group)

        traits = [
            Trait.objects.get_or_create(name=trait['name'])[0]
            for trait in traits
        ]

        animal = Animal.objects.create(**validated_data)
        animal.traits.set(traits)

        return animal

    def update(self, instance: dict, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
