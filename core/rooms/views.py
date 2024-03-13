from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuestRoomForm


def home(request):
    if request.user.is_authenticated:
        return redirect('rooms:view_rooms')
    return render(request, 'rooms/home.html')


@login_required
def view_rooms(request):
    rooms = request.user.rooms.all()
    return render(request, 'rooms/rooms.html', {'rooms': rooms})


@login_required
def create_room(request):
    form = QuestRoomForm()
    if request.method == 'POST':
        form = QuestRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.expires_at = timezone.now() + timezone.timedelta(days=room.expire_days)
            room.head = request.user
            room.save()
            return redirect('rooms:view_rooms')
    return render(request, 'rooms/create_room.html', {'form': form})
