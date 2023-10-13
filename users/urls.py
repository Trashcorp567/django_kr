from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, generate_new_password, UserListView, DeactivateUserView, verify_email

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('verify/<str:token>/', verify_email, name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/generate_pass/', generate_new_password, name='generate_new_password'),
    path('user/', UserListView.as_view(), name='user_list'),
    path('deactivate_user/<int:pk>/', DeactivateUserView.as_view(), name='client_deactivate'),
]