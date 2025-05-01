from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .serializers import PhoneNumberSerializer, OTPVerificationSerializer, UserSerializer
from .services import generate_otp, verify_otp

User = get_user_model()


class RequestOTPView(APIView):
    def post(self, request):
        print(request.data)
        print("**********************************")
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            code = generate_otp(phone_number)

            return Response({'message': 'OTP sent successfully', 'code': code}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            is_new = True
            if verify_otp(phone_number, code):
                try:
                    user = User.objects.get(phone_number=phone_number)
                    is_new= False
                except User.DoesNotExist:

                    user = User.objects.create(
                        phone_number=phone_number,
                        is_user_active=True
                    )


                refresh = RefreshToken.for_user(user)

                return Response({
                    'is_new': is_new,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data,
                }, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)