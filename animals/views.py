from functools import partial
from unittest.mock import patch
from urllib import response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
import ipdb
from animals.models import Animal

from animals.serializers import AnimalSerializer


class AnimalView(APIView):
    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AnimalDetailView(APIView):
    def get(self, request: Request, animal_id) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)
        serializer = AnimalSerializer(animal)

        return Response(serializer.data)

    def patch(self, request: Request, animal_id) -> Response:
        not_allowed_keys = ["traits", "group", "sex"]

        for key in not_allowed_keys:
            if request.data.get(key, None):
                return Response(
                    {f"{key}": f"You can not update {key} property."},
                    status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request: Request, animal_id) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status.HTTP_204_NO_CONTENT)
