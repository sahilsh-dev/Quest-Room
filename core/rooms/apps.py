from django.apps import AppConfig

class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'

    def ready(self):
        from django.db.models.signals import post_save
        from guardian.shortcuts import assign_perm
        from django.contrib.auth.models import Group
        from .models import QuestRoom
        
        def set_room_permissions(sender, instance, **kwargs):
            if kwargs['created']:
                member_group, _ = Group.objects.get_or_create(name=f'Member - Room {instance.id}')
                admin_group, _ = Group.objects.get_or_create(name=f'Admin - Room {instance.id}')
                assign_perm('rooms.view_questroom', member_group, instance)
                assign_perm('rooms.can_send_message', member_group, instance)

                assign_perm('rooms.change_questroom', admin_group, instance)
                assign_perm('rooms.can_add_user', admin_group, instance)
                assign_perm('rooms.can_remove_user', admin_group, instance)
                assign_perm('rooms.can_generate_roomcode', admin_group, instance)
                assign_perm('rooms.can_make_admin', admin_group, instance)

                admin_group.user_set.add(instance.created_by)
                member_group.user_set.add(instance.created_by)
                
        post_save.connect(set_room_permissions, sender=QuestRoom)
