# Generated by Django 5.1.2 on 2024-11-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pub', '0005_arxivcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='arxiventry',
            name='synced',
            field=models.BooleanField(default=False, verbose_name='已同步'),
        ),
        migrations.AddField(
            model_name='githubrepo',
            name='synced',
            field=models.BooleanField(default=False, verbose_name='已同步'),
        ),
    ]
