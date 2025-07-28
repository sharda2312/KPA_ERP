from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WheelSpecification
from django.db import IntegrityError
from .serializers import WheelSpecificationSerializer, WheelSpecificationListSerializer

class WheelSpecifications(APIView):
    """
    - GET: /api/forms/wheel-specifications/
    - POST: /api/forms/wheel-specifications/
    """

    def get(self, request, *args, **kwargs):
      
        queryset = WheelSpecification.objects.all()

        # Get query parameters from the request URL
        form_number = request.query_params.get('formNumber', None)
        submitted_by = request.query_params.get('submittedBy', None)
        submitted_date = request.query_params.get('submittedDate', None)

        if form_number:
            queryset = queryset.filter(form_number=form_number)
        if submitted_by:
            queryset = queryset.filter(submitted_by=submitted_by)
        if submitted_date:
            queryset = queryset.filter(submitted_date=submitted_date)

        # Serializer for the GET response
        serializer = WheelSpecificationListSerializer(queryset, many=True)
        
        response_data = {
            "success": True,
            "message": "Filtered wheel specification forms fetched successfully.",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = WheelSpecificationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                wheel_spec = serializer.save()

                response_data = {
                    "status": "success",
                    "success": True,
                    "message": "Wheel specification submitted successfully.",
                    "data": {
                        "formNumber": wheel_spec.form_number,
                        "submittedBy": wheel_spec.submitted_by,
                        "submittedDate": wheel_spec.submitted_date.isoformat(),
                        "status": "Saved"
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                if 'duplicate key value violates unique constraint' in str(e):
                    return Response({
                        "status": "error",
                        "success": False,
                        "message": "A form with this formNumber already exists.",
                        "errors": {
                            "formNumber": ["This formNumber must be unique."]
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Catch DB error
                return Response({
                    "status": "error",
                    "success": False,
                    "message": "Database integrity error.",
                    "errors": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Standard validation error
        return Response({
            "status": "error",
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)