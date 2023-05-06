from django.urls import path
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .views import register, login, logout

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
