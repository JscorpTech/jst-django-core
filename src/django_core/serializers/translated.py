from django.conf import settings
from rest_framework import serializers


class AbstractTranslatedSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """
        Override to_representation to add translated fields to the response.
        """
        representation = super().to_representation(instance)
        for field in self.Meta.translated_fields:
            for lang, _ in settings.LANGUAGES:
                translated_field = f"{field}_{lang}"
                representation[translated_field] = getattr(instance, translated_field)
        return representation

    def to_internal_value(self, data):
        """
        Override to_internal_value to process translated fields from the input data.
        For each field in Meta.translated_fields, generate a translated field name
        by appending the language code, and add this translated field to the internal
        value if it exists in the input data.
        """
        internal_value = super().to_internal_value(data)
        for field in self.Meta.translated_fields:
            for lang, _ in settings.LANGUAGES:
                translated_field = f"{field}_{lang}"
                if translated_field in data:
                    internal_value[translated_field] = data[translated_field]
        return internal_value
