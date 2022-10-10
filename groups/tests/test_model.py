from groups.models import Group
from django.test import TestCase


class GroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.group_data = {
            "name": "cao",
            "scientific_name": "canis familiaris"
        }

        cls.group = Group(**cls.group_data)
        cls.group.save()

    def test_name_max_length(self):
        max_length = self.group._meta.get_field('name').max_length

        self.assertEqual(max_length, 20)

    def test_scientific_name_max_length(self):
        max_length = self.group._meta.get_field('scientific_name').max_length

        self.assertEqual(max_length, 50)

    def test_name_unique_constraint(self):
        unique = self.group._meta.get_field('name').unique

        self.assertTrue(unique)

    def test_scientific_name_unique_constraint(self):
        unique = self.group._meta.get_field('scientific_name').unique

        self.assertTrue(unique)
