from django.urls import path

from account.views import RegisterView, ActivationView, PasswordResetView, CompleteResetPasswordView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset_complete/', CompleteResetPasswordView.as_view()),
]

#TODO: ask about logout, how it should be impemented correctly