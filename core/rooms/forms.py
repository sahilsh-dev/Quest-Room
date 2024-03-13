from django.forms import ModelForm
from .models import QuestRoom


class QuestRoomForm(ModelForm):
    class Meta:
        model = QuestRoom
        fields = ['name', 'description', 'expire_days', 'room_type', 'daily_required_points']