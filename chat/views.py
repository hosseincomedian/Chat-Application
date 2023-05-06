from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required




class room(View):
    def get(self, reqest, room_name):
        context = {
            'room_name': room_name
        }
        return render(reqest, 'chat/test_room.html', context)
