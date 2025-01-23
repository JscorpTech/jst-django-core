from django.conf import settings
from rest_framework import serializers


class AbstractTranslatedSerializer(serializers.ModelSerializer):
    """
    Serializer for models with translated fields. Automatically handles translation
    fields based on settings.LANGUAGES.
    """

    def _translate_json(self, instance, field):
        """
        Generates a dictionary with translations for a given field.

        :param instance: The model instance.
        :param field: The base field name.
        :return: A dictionary of translations, e.g., {'en': value, 'uz': value}.
        """
        return {lang: getattr(instance, f"{field}_{lang}", None) for lang, _ in settings.LANGUAGES}

    def to_representation(self, instance):
        """
        Customizes the serialized representation of the instance.

        :param instance: The model instance.
        :return: A dictionary representation of the instance.
        """
        representation = super().to_representation(instance)

        translated_fields = getattr(self.Meta, "translated_fields", [])
        translation_mode = getattr(self.Meta, "translated", 0)  # Default to 0

        for field in translated_fields:
            if translation_mode == 1:
                representation[field] = self._translate_json(instance, field)
            elif translation_mode == 2:
                for lang, _ in settings.LANGUAGES:
                    field_name = f"{field}_{lang}"
                    representation[field_name] = getattr(instance, field_name, None)

        return representation

    def to_internal_value(self, data):
        """
        Converts incoming data to a validated dictionary suitable for the model.

        :param data: The input data.
        :return: A validated dictionary of field values.
        """
        data = data.copy()
        if not isinstance(data, dict):
            return data
        translated_fields = getattr(self.Meta, "translated_fields", [])
        for field in translated_fields:
            value = data.get(f"{field}_{settings.LANGUAGE_CODE}", data.get(field, None))
            if value is not None:
                data[field] = value
        internal_value = super().to_internal_value(data)
        for field in translated_fields:
            for lang, _ in settings.LANGUAGES:
                translated_field = f"{field}_{lang}"
                if translated_field in data:
                    internal_value[translated_field] = data[translated_field]

        return internal_value
