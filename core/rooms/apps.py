from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm

class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'

    def ready(self):
        from .models import QuestRoom
        
        def set_room_owner_permissions(sender, instance, **kwargs):
            if kwargs['created']:
                instance.admins.add(instance.created_by)
                instance.members.add(instance.created_by)
                instance.save()

                member_group, _ = Group.objects.get_or_create(name=f'Member - Room {instance.id}')
                admin_group, _ = Group.objects.get_or_create(name=f'Admin - Room {instance.id}')
                assign_perm('rooms.can_send_message', member_group, instance)
                assign_perm('rooms.can_add_user', admin_group, instance)
                assign_perm('rooms.can_remove_user', admin_group, instance)

                admin_group.user_set.add(instance.created_by)
                member_group.user_set.add(instance.created_by)
                
        post_save.connect(set_room_owner_permissions, sender=QuestRoom)