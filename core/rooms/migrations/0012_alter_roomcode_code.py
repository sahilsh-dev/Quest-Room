# Generated by Django 5.0.3 on 2024-03-17 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0011_questroom_admins_alter_questroom_members_roomcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomcode',
            name='code',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]