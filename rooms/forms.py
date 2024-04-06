from django import forms
from .models import QuestRoom

class QuestRoomForm(forms.ModelForm):
    class Meta:
        model = QuestRoom
        fields = ['name', 'description', 'expire_days', 'room_type']

