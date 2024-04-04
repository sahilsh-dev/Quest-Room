# Generated by Django 5.0.3 on 2024-03-17 09:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0010_alter_message_managers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='questroom',
            name='admins',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questroom',
            name='members',
            field=models.ManyToManyField(related_name='joined_rooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RoomCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('generated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rooms.questroom')),
            ],
        ),
    ]