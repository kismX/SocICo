# Generated by Django 4.2.7 on 2024-01-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_rename_type_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_sent',
            field=models.BooleanField(default=False),
        ),
    ]
