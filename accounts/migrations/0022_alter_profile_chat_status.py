# Generated by Django 4.2.7 on 2024-01-30 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_profile_chat_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='chat_status',
            field=models.TextField(default='offline'),
        ),
    ]
