# Generated by Django 4.2.7 on 2023-11-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interests',
            field=models.TextField(blank=True, help_text='Gib interessen getrennt durch Komma an'),
        ),
    ]
