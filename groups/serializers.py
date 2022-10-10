from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from groups.models import Group


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(
        max_length=20
    )
    scientific_name = serializers.CharField(
        max_length=50
    )
