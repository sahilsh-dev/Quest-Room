from django.contrib import admin
from .models import QuestRoom, Message
from guardian.admin import GuardedModelAdmin 

@admin.register(QuestRoom)
class QuestRoomAdmin(GuardedModelAdmin):
    readonly_fields = ['id']
    pass


@admin.register(Message)
class MessageAdmin(GuardedModelAdmin):
    pass
