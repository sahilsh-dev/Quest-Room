from django.forms import ModelForm
from .models import QuestRoom

class QuestRoomForm(ModelForm):
    class Meta:
        model = QuestRoom
        fields = ['name', 'description', 'room_type', 'expire_days', 'daily_required_points']