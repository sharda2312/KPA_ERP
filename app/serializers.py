# In your Django app's serializers.py file

from rest_framework import serializers
from .models import WheelSpecification

class FieldsSerializer(serializers.Serializer):
    """
    A serializer specifically for the nested 'fields' object.
    This provides validation for the inner fields of the JSON payload.
    It does not map to a model directly, so it inherits from the base Serializer class.
    """
    treadDiameterNew = serializers.CharField(max_length=100)
    lastShopIssueSize = serializers.CharField(max_length=100)
    condemningDia = serializers.CharField(max_length=100)
    wheelGauge = serializers.CharField(max_length=100)
    variationSameAxle = serializers.CharField(max_length=100)
    variationSameBogie = serializers.CharField(max_length=100)
    variationSameCoach = serializers.CharField(max_length=100)
    wheelProfile = serializers.CharField(max_length=100)
    intermediateWWP = serializers.CharField(max_length=100)
    bearingSeatDiameter = serializers.CharField(max_length=100)
    rollerBearingOuterDia = serializers.CharField(max_length=100)
    rollerBearingBoreDia = serializers.CharField(max_length=100)
    rollerBearingWidth = serializers.CharField(max_length=100)
    axleBoxHousingBoreDia = serializers.CharField(max_length=100)
    wheelDiscWidth = serializers.CharField(max_length=100)


class WheelSpecificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the WheelSpecification model.
    Handles the conversion between JSON (camelCase) and the model (snake_case).
    """
    # Use the 'source' argument to map the API's camelCase field names
    # to the model's snake_case field names.
    formNumber = serializers.CharField(source='form_number')
    submittedBy = serializers.CharField(source='submitted_by')
    submittedDate = serializers.DateField(source='submitted_date')

    # Nest the FieldsSerializer to handle the 'fields' object.
    fields = FieldsSerializer()

    class Meta:
        model = WheelSpecification
        # List the fields that the API should expose.
        # These are the public-facing (camelCase) names.
        fields = [
            'formNumber',
            'submittedBy',
        'submittedDate',
            'fields'
        ]

    def create(self, validated_data):
        """
        Custom create method to handle saving the nested 'fields' data correctly.
        """
        # Pop the nested 'fields' data from the validated data.
        fields_data = validated_data.pop('fields')
        
        # Create the WheelSpecification instance with the remaining data.
        # The 'source' mapping handles the field name conversion automatically.
        wheel_spec = WheelSpecification.objects.create(fields=fields_data, **validated_data)
        
        return wheel_spec
    
class WheelSpecificationListSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for the list view (GET).
    It returns only a subset of the nested 'fields' data.
    """
    formNumber = serializers.CharField(source='form_number')
    submittedBy = serializers.CharField(source='submitted_by')
    submittedDate = serializers.DateField(source='submitted_date')

    # 1. Renamed from 'fields' to 'field_summary' to avoid conflict
    field_summary = serializers.SerializerMethodField()

    class Meta:
        model = WheelSpecification
        fields = [
            'formNumber',
            'submittedBy',
            'submittedDate',
            'field_summary'  # 3. Updated the name in the list
        ]

    # 2. Renamed method from 'get_fields' to 'get_field_summary'
    def get_field_summary(self, obj):
        """
        This method manually creates the 'field_summary' object for the response.
        'obj' is the WheelSpecification instance being serialized.
        """
        full_fields = obj.fields or {}
        return {
            'treadDiameterNew': full_fields.get('treadDiameterNew'),
            'lastShopIssueSize': full_fields.get('lastShopIssueSize'),
            'condemningDia': full_fields.get('condemningDia'),
            'wheelGauge': full_fields.get('wheelGauge')
        }

