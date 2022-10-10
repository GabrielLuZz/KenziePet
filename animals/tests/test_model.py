import math
from animals.models import Animal
from django.test import TestCase

from groups.models import Group
from traits.models import Trait


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.animal_data = {
            "name": "George",
            "age": 10,
            "weight": 30.0,
            "sex": "Macho"
        }

        cls.animal_data2 = {
            "name": "gloria",
            "age": 15,
            "weight": 25.0,
            "sex": "Fêmea"
        }

        cls.group_data = {
            "name": "cao",
            "scientific_name": "canis familiaris"
        }

        cls.group = Group(**cls.group_data)
        cls.group.save()

        cls.animal = Animal.objects.create(**cls.animal_data, group=cls.group)

    def test_name_max_length(self):
        max_length = self.animal._meta.get_field('name').max_length

        self.assertEqual(max_length, 50)

    def test_sex_max_length(self):
        max_length = self.animal._meta.get_field('sex').max_length

        self.assertEqual(max_length, 15)

    def test_convert_dog_age_to_human_years(self):
        result = self.animal.convert_dog_age_to_human_years()
        expected = (16 * math.log(self.animal.age)) + 31

        self.assertEqual(expected, result)

    def test_animal_fields(self):
        self.assertEqual(self.animal.name, self.animal_data["name"])
        self.assertEqual(self.animal.age, self.animal_data["age"])
        self.assertEqual(self.animal.weight, self.animal_data["weight"])
        self.assertEqual(self.animal.sex, self.animal_data["sex"])

    def test_group_may_contain_multiple_animals(self):

        animal2 = Animal.objects.create(**self.animal_data2, group=self.group)

        self.assertEquals(
            2,
            self.group.animals.count()
        )

        self.assertIs(self.animal.group, self.group)
        self.assertIs(animal2.group, self.group)

    def test_animal_cannot_belong_to_more_than_one_group(self):

        group2 = Group.objects.create(
            name='Outra Produtora',
            scientific_name="nova produtora"
        )
        self.animal.group = group2
        self.animal.save()

        self.assertNotIn(self.animal, self.group.animals.all())
        self.assertIn(self.animal, group2.animals.all())

    def test_trait_can_be_attached_to_multiple_animals(self):

        animal2 = Animal.objects.create(**self.animal_data2, group=self.group)
        trait = Trait.objects.create(name="velho")

        trait.animals.add(self.animal)
        trait.animals.add(animal2)

        self.assertEquals(2, trait.animals.count())

        self.assertIn(trait, self.animal.traits.all())
        self.assertIn(trait, animal2.traits.all())
