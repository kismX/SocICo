# Generated by Django 4.2.7 on 2024-01-11 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_customuser_city_customuser_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='country',
        ),
    ]