# Generated by Django 5.1.2 on 2024-11-13 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='intro',
            field=models.TextField(blank=True, verbose_name='个人简介'),
        ),
        migrations.AddField(
            model_name='user',
            name='scholar_url',
            field=models.URLField(blank=True, max_length=255, verbose_name='学术主页'),
        ),
        migrations.AddField(
            model_name='user',
            name='view_count',
            field=models.IntegerField(default=0, verbose_name='浏览次数'),
        ),
    ]
