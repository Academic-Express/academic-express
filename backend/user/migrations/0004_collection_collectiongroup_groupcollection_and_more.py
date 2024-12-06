# Generated by Django 4.2.5 on 2024-12-05 16:29

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
                ('item_type', models.CharField(choices=[('arxiv', 'ArXiv Paper'), ('github', 'GitHub Repository')], default='arxiv', max_length=10)),
                ('item_id', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collection_item',
                'unique_together': {('user', 'item_type', 'item_id')},
            },
        ),
        migrations.CreateModel(
            name='CollectionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'collection_group',
            },
        ),
        migrations.CreateModel(
            name='GroupCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.collection')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.collectiongroup')),
            ],
            options={
                'db_table': 'collection_group_item',
                'unique_together': {('group', 'collection')},
            },
        ),
        migrations.AddField(
            model_name='collectiongroup',
            name='collections',
            field=models.ManyToManyField(through='user.GroupCollection', to='user.collection'),
        ),
        migrations.AddField(
            model_name='collectiongroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='collectiongroup',
            unique_together={('user', 'name')},
        ),
    ]
