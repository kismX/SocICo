# Generated by Django 4.2.7 on 2024-01-24 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_remove_comment_notification_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='notification_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
