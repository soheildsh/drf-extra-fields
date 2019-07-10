from rest_framework import serializers
from rest_framework.test import APISimpleTestCase

from drf_extra_fields.relations import (
    PresentablePrimaryKeyRelatedField,
    PresentableSlugRelatedField,
)
from .utils import MockObject, MockQueryset


class PresentationSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {"pk": instance.pk, "name": instance.name}


class TestPresentablePrimaryKeyRelatedField(APISimpleTestCase):
    def setUp(self):
        self.queryset = MockQueryset(
            [
                MockObject(pk=1, name="foo"),
                MockObject(pk=2, name="bar"),
                MockObject(pk=3, name="baz"),
            ]
        )
        self.instance = self.queryset.items[2]
        self.field = PresentablePrimaryKeyRelatedField(
            queryset=self.queryset, presentation_serializer=PresentationSerializer
        )

    def test_representation(self):
        representation = self.field.to_representation(self.instance)
        expected_representation = PresentationSerializer(self.instance).data
        assert representation == expected_representation


class TestPresentableSlugRelatedField(APISimpleTestCase):
    def setUp(self):
        self.queryset = MockQueryset(
            [
                MockObject(pk=1, name="foo"),
                MockObject(pk=2, name="bar"),
                MockObject(pk=3, name="baz"),
            ]
        )
        self.instance = self.queryset.items[2]
        self.field = PresentableSlugRelatedField(
            slug_field="name",
            queryset=self.queryset,
            presentation_serializer=PresentationSerializer,
        )

    def test_representation(self):
        representation = self.field.to_representation(self.instance)
        expected_representation = PresentationSerializer(self.instance).data
        assert representation == expected_representation
