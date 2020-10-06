from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (LoginView, LogoutView, home, forgot_password, PasswordResetView,)

app_name = 'User'

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]