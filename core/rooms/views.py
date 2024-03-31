import secrets
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group
from guardian.decorators import permission_required_or_403
from .forms import QuestRoomForm
from .models import QuestRoom, Message, RoomCode


def home(request):
    if request.user.is_authenticated:
        return redirect('rooms:view_rooms')
    return render(request, 'rooms/home.html')


@login_required
def view_rooms(request):
    created_rooms = QuestRoom.objects.filter(created_by=request.user)
    joined_rooms = QuestRoom.objects.filter(members=request.user)
    joined_rooms = joined_rooms.exclude(created_by=request.user)
    return render(
        request, 
        'rooms/user_rooms.html', {
            'created_rooms': created_rooms,
            'joined_rooms': joined_rooms,
        }
    )


@login_required
def create_room(request):
    form = QuestRoomForm()
    if request.method == 'POST':
        form = QuestRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['name']
            if QuestRoom.objects.filter(name=room_name, created_by=request.user).exists():
                form.add_error('name', 'Room with this name already exists')
                return render(request, 'rooms/create_room.html', {'form': form})

            room = form.save(commit=False)
            room.created_by = request.user
            room.expires_at = timezone.now() + timezone.timedelta(days=room.expire_days)
            room.save()
            room.admins.add(room.created_by)
            room.members.add(room.created_by)
            room.save()
            return redirect('rooms:view_rooms')
    return render(request, 'rooms/create_room.html', {'form': form})


@login_required
@permission_required_or_403('rooms.view_questroom', (QuestRoom, 'id', 'room_id'))
def room_detail(request, room_id):
    room = get_object_or_404(QuestRoom, pk=room_id)
    if request.user in room.members.all():
        latest_messages = Message.latest_messages.get_latest_messages(room_id)
        has_perm_make_admin = request.user.has_perm('rooms.can_make_admin', room)
        has_perm_remove_user = request.user.has_perm('rooms.can_remove_user', room)
        has_perm_generate_roomcode = request.user.has_perm('rooms.can_generate_roomcode', room)        
        return render (
            request, 
            'rooms/room_detail.html', {
                'room': room,
                'latest_messages': latest_messages,
                'has_perm_make_admin': has_perm_make_admin,
                'has_perm_remove_user': has_perm_remove_user,
                'has_perm_generate_roomcode': has_perm_generate_roomcode,
            }
        )
    messages.error(request, 'You are not a member of this room')
    return redirect('rooms:view_rooms')


@login_required
@permission_required_or_403('rooms.can_generate_roomcode', (QuestRoom, 'id', 'room_id'))
def generate_room_code(request, room_id): 
    if request.method == 'POST':
        upper_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        random_str = ''.join(secrets.choice(upper_chars) for _ in range(settings.ROOM_INVITE_CODE_LENGTH))
        code = (random_str + str(room_id))[-settings.ROOM_INVITE_CODE_LENGTH:]
        room_code = RoomCode.objects.create(room_id=room_id, code=code, generated_by=request.user)
        room_code.save()
        return JsonResponse({'code': code})
    return JsonResponse({'error': 'Only admins can generate room code'})


@login_required
def join_room(request):
    if request.method == 'POST':
        room_code_text = request.POST.get('room_code')
        room_code = RoomCode.objects.filter(code=room_code_text).first()
        if room_code and room_code.is_valid():
            room = room_code.room 
            room.members.add(request.user)
            room_member_group = Group.objects.get(name=f'Member - Room {room.id}')
            request.user.groups.add(room_member_group)
            return redirect('rooms:room_detail', room_id=room_code.room.id)
    return redirect('rooms:view_rooms')
