# Generated by Django 5.0.3 on 2024-03-27 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0014_rename_room_id_roomcode_room'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questroom',
            options={'permissions': [('can_remove_user', 'Can remove user from room'), ('can_add_user', 'Can add user to room'), ('can_change_room', 'Can change room settings')]},
        ),
    ]