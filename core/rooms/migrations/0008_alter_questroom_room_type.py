# Generated by Django 5.0.3 on 2024-03-15 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0007_rename_head_questroom_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questroom',
            name='room_type',
            field=models.CharField(choices=[('LC', 'Leetcode')], default='LC', max_length=2),
        ),
    ]
