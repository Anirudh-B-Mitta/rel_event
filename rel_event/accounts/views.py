# views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import account_activation_token


class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            'access_token': access_token,
            'user': UserSerializer(user).data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    
    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token})
    

# def custom_password_reset_done_view(request):
#     return render(request, 'registration/password_reset_done.html')


class PasswordResetAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a token and send the reset email
        token = account_activation_token.make_token(user)
        reset_link = f'{settings.FRONTEND_URL}/api/password-update/{user.id}/{token}/'

        subject = 'Password Reset'
        message = f'Click on the link below to reset your password:\n{reset_link}'

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)


class PasswordUpdateAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

# # views.py
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
# from rest_framework.exceptions import PermissionDenied
# from django.contrib.auth import authenticate, login
# from .serializers import PasswordUpdateSerializer

# class PasswordUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, *args, **kwargs):
#         serializer = PasswordUpdateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = request.user
#         old_password = serializer.validated_data.get('old_password')
#         new_password = serializer.validated_data.get('new_password')

#         # Authenticate user with old password
#         if not user.check_password(old_password):
#             raise PermissionDenied(detail="Old password is incorrect.", code=status.HTTP_403_FORBIDDEN)

#         # Set and save the new password
#         user.set_password(new_password)
#         user.save()

#         # Re-authenticate the user with the new password
#         authenticated_user = authenticate(request, username=user.email, password=new_password)
#         if authenticated_user:
#             login(request, authenticated_user)

#         return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
