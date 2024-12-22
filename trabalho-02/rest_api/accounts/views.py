from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from .models import AccountsConnection
from django.core.exceptions import ValidationError

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'user created successfully' }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AccountsConnectionView(APIView): 
    def create_connection(user, connection_id):
        try:
            AccountsConnection.objects.create(user = user, connection_id=connection_id)
            return Response({'message': 'connection created successfully' } , status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response ({'message': 'max concurrent connections reached' }, status=status.HTTP_400_BAD_REQUEST)
