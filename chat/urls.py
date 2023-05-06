from django.urls import path
from .views import room
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('<str:room_name>/', login_required(room.as_view()), name='room'),
]
