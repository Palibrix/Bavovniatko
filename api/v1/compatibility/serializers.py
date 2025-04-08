from rest_framework import serializers


class ConfigurationSerializer(serializers.Serializer):
    """
    Serializer for drone component configuration
    """
    configuration = serializers.DictField(
        child=serializers.IntegerField(allow_null=True),
        required=True
    )
    previous_configuration = serializers.DictField(
        child=serializers.IntegerField(allow_null=True),
        required=False,
        allow_null=True
    )
    previous_results = serializers.DictField(required=False, allow_null=True)


class CompatibilityIssueSerializer(serializers.Serializer):
    """
    Serializer for compatibility issues
    """
    type = serializers.CharField()
    severity = serializers.CharField()
    message = serializers.CharField()
    component_refs = serializers.ListField(child=serializers.CharField())


class ComponentCompatibilitySerializer(serializers.Serializer):
    """
    Serializer for component compatibility results
    """
    is_compatible = serializers.BooleanField()
    issues = serializers.ListField(child=CompatibilityIssueSerializer())


class ConfigurationCheckSerializer(serializers.Serializer):
    """
    Serializer for compatibility check including previous state
    """
    configuration = serializers.DictField(
        child=serializers.IntegerField(allow_null=True),
        required=True
    )
    previous_configuration = serializers.DictField(
        child=serializers.IntegerField(allow_null=True),
        required=False,
        allow_null=True
    )
    previous_results = serializers.DictField(required=False, allow_null=True)