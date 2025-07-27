# In your Django app's views.py file

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WheelSpecification
from .serializers import WheelSpecificationSerializer, WheelSpecificationListSerializer

class WheelSpecifications(APIView):
    """
    API View to handle listing, filtering, and creating Wheel Specifications.
    - GET: /api/forms/wheel-specifications/
    - POST: /api/forms/wheel-specifications/
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to list and filter wheel specifications.
        Supports filtering by 'formNumber', 'submittedBy', and 'submittedDate'.
        Returns a limited subset of the 'fields' object as requested.
        """
        # Start with all objects
        queryset = WheelSpecification.objects.all()

        # Get query parameters from the request URL
        form_number = request.query_params.get('formNumber', None)
        submitted_by = request.query_params.get('submittedBy', None)
        submitted_date = request.query_params.get('submittedDate', None)

        # Apply filters if they are provided in the query parameters
        if form_number:
            queryset = queryset.filter(form_number=form_number)
        if submitted_by:
            queryset = queryset.filter(submitted_by=submitted_by)
        if submitted_date:
            queryset = queryset.filter(submitted_date=submitted_date)

        # Use the NEW lightweight serializer for the GET response
        serializer = WheelSpecificationListSerializer(queryset, many=True)
        
        response_data = {
            "success": True,
            "message": "Filtered wheel specification forms fetched successfully.",
            "data": serializer.data # <-- No more manual looping needed!
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new wheel specification.
        """
        serializer = WheelSpecificationSerializer(data=request.data)
        
        # Validate the incoming data
        if serializer.is_valid():
            # If valid, save the object. This calls the custom .create() method
            # in the serializer to handle the nested JSON.
            wheel_spec = serializer.save()
            
            # Format the success response to match the Postman collection
            response_data = {
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
        
        # If the data is not valid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

