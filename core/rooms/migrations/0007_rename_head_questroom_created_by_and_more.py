# Generated by Django 5.0.3 on 2024-03-15 14:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_alter_questroom_name_alter_questroom_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='questroom',
            old_name='head',
            new_name='created_by',
        ),
        migrations.AlterUniqueTogether(
            name='questroom',
            unique_together={('name', 'created_by')},
        ),
    ]
