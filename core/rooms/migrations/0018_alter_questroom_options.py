# Generated by Django 5.0.3 on 2024-03-27 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0017_alter_questroom_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questroom',
            options={'permissions': [('can_send_message', 'Can send message in room'), ('can_remove_user', 'Can remove user from room'), ('can_add_user', 'Can add user to room'), ('can_generate_roomcode', 'Can generate room code')]},
        ),
    ]
