# urls.py
from django.urls import path, include
from .views import SignUpView, LoginView
from .views import PasswordResetAPIView, PasswordUpdateAPIView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', PasswordResetAPIView.as_view(), name='password_reset_api'),
    path('password-update/<int:pk>/<token>/', PasswordUpdateAPIView.as_view(), name='password_update_api'),  #add frontend url later
]
