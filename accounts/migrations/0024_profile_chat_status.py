# Generated by Django 4.2.7 on 2024-01-31 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_remove_profile_chat_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='chat_status',
            field=models.BooleanField(default=False),
        ),
    ]