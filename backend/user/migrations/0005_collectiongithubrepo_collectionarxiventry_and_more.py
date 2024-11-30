# Generated by Django 4.2.5 on 2024-11-30 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pub', '__first__'),
        ('user', '0004_collection_collectionitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionGithubRepo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_time', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.collection')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pub.githubrepo')),
            ],
            options={
                'unique_together': {('collection', 'repo')},
            },
        ),
        migrations.CreateModel(
            name='CollectionArxivEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_time', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.collection')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pub.arxiventry')),
            ],
            options={
                'unique_together': {('collection', 'entry')},
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='arxiv_entries',
            field=models.ManyToManyField(through='user.CollectionArxivEntry', to='pub.arxiventry'),
        ),
        migrations.AddField(
            model_name='collection',
            name='github_repos',
            field=models.ManyToManyField(through='user.CollectionGithubRepo', to='pub.githubrepo'),
        ),
    ]
