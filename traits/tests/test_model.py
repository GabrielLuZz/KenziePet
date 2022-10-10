from traits.models import Trait
from django.test import TestCase


class TraitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.trait_data = {
            "name": "lindo"
        }

        cls.trait = Trait(**cls.trait_data)
        cls.trait.save()

    def test_name_max_length(self):
        max_length = self.trait._meta.get_field('name').max_length

        self.assertEqual(max_length, 20)

    def test_name_unique_constraint(self):
        unique = self.trait._meta.get_field('name').unique

        self.assertTrue(unique)
