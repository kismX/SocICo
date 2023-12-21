# Generated by Django 4.2.7 on 2023-12-21 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_category', models.CharField(max_length=100, unique=True)),
                ('term_category_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, unique=True)),
                ('usage_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='searchers.categorymodel')),
                ('synonyms', models.ManyToManyField(to='searchers.terms')),
            ],
        ),
    ]
