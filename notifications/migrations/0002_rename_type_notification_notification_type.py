# Generated by Django 4.2.7 on 2024-01-06 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='type',
            new_name='notification_type',
        ),
    ]
