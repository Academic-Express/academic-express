# Generated by Django 4.2.5 on 2024-11-30 14:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('arxiv', 'ArXiv Paper'), ('github', 'GitHub Repository')], max_length=10)),
                ('item_id', models.CharField(max_length=100)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.collection')),
            ],
            options={
                'unique_together': {('collection', 'item_type', 'item_id')},
            },
        ),
    ]
