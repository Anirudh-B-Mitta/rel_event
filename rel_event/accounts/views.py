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
from rest_framework.permissions import IsAuthenticated
from .serializers import PasswordUpdateSerializer
from django.core.mail import EmailMessage
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render


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
    

class PasswordResetAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        print(email, "HI")

        if not email:
            print("HI 1")
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
            print("HI 2")
        except User.DoesNotExist:
            print("HI 3")
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a token and send the reset email
        token = account_activation_token.make_hash_value(user)
        print("HI 4")
        reset_link = f'{settings.FRONTEND_URL}/pwdUpdate/{user.id}/{token}/'
        print(reset_link, "HI 5")

        # subject = 'Password Reset'
        # message = f'Click on the link below to reset your password:\n{reset_link}'

        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        
        # Render the HTML template
        context = {'reset_link': reset_link, 'name': user.name}
        html_message = render(request, 'accounts/forgot_password.html', context).content.decode('utf-8')

        subject = 'Password Reset'
        
        # Send the HTML email
        email = EmailMessage(subject, '', settings.DEFAULT_FROM_EMAIL, [email])
        email.content_subtype = 'html'  # Set the content type to HTML
        email.body = html_message

        # Send the email
        email.send()

        print("Final HI")

        return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)


class PasswordUpdateAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PasswordUpdateSerializer
    
    def get_object(self):
        user_id = self.kwargs.get('pk')
        token = self.kwargs.get('token')

        User = get_user_model()

        try:
            user = User.objects.get(pk=user_id)
            token_generator = account_activation_token.make_hash_value(user)
            if str(token_generator) == token:
                return user
        except User.DoesNotExist:
            return Response({'message': "user doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return None


    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({'error': 'User not found or unauthorized'}, status=404)
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            new_password = serializer.validated_data['password']
            # Set password for the user instance before saving
            serializer.instance.set_password(new_password)
            serializer.instance.save()
        else:
            serializer.save()


class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    parser_classes = (MultiPartParser, FormParser,)  # Allow file uploads

    def put(self, request, *args, **kwargs):
        new_name = request.data.get('name')
        new_image = request.data.get('profile_pic')

        if new_name:
            request.user.name = new_name

        if new_image:
            request.user.profile_pic = new_image

        request.user.save()

        print(request.data  )

        response_data = {
            'id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'image_url': request.user.profile_pic.url if request.user.profile_pic else None,
            'message': 'Profile updated successfully'
        }
        return Response(response_data)

    def get(self, request):
        return Response(UserSerializer(instance = request.user, context={'request': request}).data, status=status.HTTP_200_OK)
