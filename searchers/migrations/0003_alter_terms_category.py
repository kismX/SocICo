# Generated by Django 4.2.7 on 2023-12-21 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchers', '0002_alter_terms_synonyms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terms',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='searchers.categorymodel'),
        ),
    ]
