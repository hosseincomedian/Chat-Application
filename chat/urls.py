from django.urls import path
from .views import index, room
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', index.as_view(), name='create_room'),
    path('<str:room_name>/', login_required(room.as_view()), name='room'),
]
