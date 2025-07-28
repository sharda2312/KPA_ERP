from rest_framework import serializers
from .models import WheelSpecification

class FieldsSerializer(serializers.Serializer):
    # A serializer specifically for the nested 'fields' object.
    
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
    # Serializer for the WheelSpecification model.
      
    formNumber = serializers.CharField(source='form_number')
    submittedBy = serializers.CharField(source='submitted_by')
    submittedDate = serializers.DateField(source='submitted_date')

    # Nest the FieldsSerializer to handle the 'fields' object.
    fields = FieldsSerializer()

    class Meta:
        model = WheelSpecification
        fields = [
            'formNumber',
            'submittedBy',
        'submittedDate',
            'fields'
        ]

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        
        wheel_spec = WheelSpecification.objects.create(fields=fields_data, **validated_data)
        
        return wheel_spec
    
class WheelSpecificationListSerializer(serializers.ModelSerializer):
    # A serializer for GET.
    
    formNumber = serializers.CharField(source='form_number')
    submittedBy = serializers.CharField(source='submitted_by')
    submittedDate = serializers.DateField(source='submitted_date')

    field_summary = serializers.SerializerMethodField()

    class Meta:
        model = WheelSpecification
        fields = [
            'formNumber',
            'submittedBy',
            'submittedDate',
            'field_summary' 
        ]

    def get_field_summary(self, obj):
       
        full_fields = obj.fields or {}
        return {
            'treadDiameterNew': full_fields.get('treadDiameterNew'),
            'lastShopIssueSize': full_fields.get('lastShopIssueSize'),
            'condemningDia': full_fields.get('condemningDia'),
            'wheelGauge': full_fields.get('wheelGauge')
        }

