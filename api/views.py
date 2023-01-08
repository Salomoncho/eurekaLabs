from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from api import api_messages
from api.permissions import ValidateAPIKeyAccess
from api.utils import process_alphavantage_data, validate_response
import requests


class RegisterAPIView(APIView):
    """Register Endpoint returns the API Key for the Stock Service if a new user is successfully registered"""
    serializer_class = serializers.RegisterSerializer
    throttle_scope = 'limit_per_minute'

    def post(self, request):
        """Method to validate and register a new user."""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                user = get_user_model().objects.create_user(
                                                            username=serializer.validated_data.get('name'),
                                                            last_name=serializer.validated_data.get('last_name'),
                                                            email=serializer.validated_data.get('email'),
                                                            password=serializer.validated_data.get('password')
                )
                user.save()
            except Exception:
                return Response(
                    {'error': api_messages.REGISTER_ERROR_CREATING_USER}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            try:
                get_user_model().objects.get(
                    username=serializer.validated_data.get('name'),
                    last_name=serializer.validated_data.get('last_name'),
                    email=serializer.validated_data.get('email')
                )
                return Response(
                    {'message': api_messages.REGISTER_USER_CREATED, 'API_KEY': settings.STOCK_SERVICE_API_KEY},
                    status=status.HTTP_201_CREATED
                )
            except get_user_model().DoesNotExist:
                return Response(
                    {'error': api_messages.REGISTER_USER_NOT_CREATED}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """Login Endpoint returns the API Key for the Stock Service if user exist"""

    serializer_class = serializers.LoginSerializer
    throttle_scope = 'limit_per_minute'

    def post(self, request):
        """Method to login into the service."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                user = get_user_model().objects.get(email=serializer.validated_data.get('email'))
                if user.check_password(serializer.validated_data.get('password')):
                    return Response(
                        {'message': api_messages.LOGIN_USER_AUTHENTICATED, 'API_KEY': settings.STOCK_SERVICE_API_KEY}
                    )
                else:
                    return Response({'message': api_messages.LOGIN_PASS_INCORRECT}, status=status.HTTP_400_BAD_REQUEST)
            except get_user_model().DoesNotExist:
                return Response({'message': api_messages.LOGIN_USER_DOES_NOT_EXIST}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockServiceAPIView(APIView):
    """ Stock Service API """

    permission_classes = (ValidateAPIKeyAccess,)
    serializer_class = serializers.StockServiceSerializer
    throttle_scope = 'limit_per_minute'

    def post(self, request):
        """Method to send a request to the *Alpha Vantage API* by STOCK Name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&' \
                  f'symbol={serializer.validated_data.get("stock_symbol")}&apikey={settings.ALPHA_VANTAGE_API_KEY}'
            resp = requests.get(url)

            valid_data = validate_response(resp.json())
            if not valid_data.get('data'):
                return Response({'error': valid_data['error']}, status=valid_data['status'])
            data = process_alphavantage_data(valid_data.get('data'))

            return Response({'data': data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
