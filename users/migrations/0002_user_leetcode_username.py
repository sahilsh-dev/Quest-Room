# Generated by Django 5.0.3 on 2024-04-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='leetcode_username',
            field=models.CharField(default='core_light', max_length=50),
            preserve_default=False,
        ),
    ]
