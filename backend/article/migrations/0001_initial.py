# Generated by Django 3.1.7 on 2021-03-16 08:09

import backend.article.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=100, verbose_name='Title')),
                ('description', models.TextField(blank=True, default='', max_length=4000, verbose_name='Description')),
                ('short_description', models.TextField(blank=True, default='', max_length=400, verbose_name='Short description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
                ('cover', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='filer.image', verbose_name='Cover')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000, validators=[backend.article.validators.validate_comment], verbose_name='Comment text')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created at')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='article.article', verbose_name='Article')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Comment creator')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='article.articlecomment', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Article comment',
                'verbose_name_plural': 'Article comments',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='article.article', verbose_name='Article')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filer.image', verbose_name='Article image')),
            ],
            options={
                'verbose_name': 'Article Image',
                'verbose_name_plural': 'Article Images',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ArticleCommentLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='article.articlecomment', verbose_name='Comment')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Like creator')),
            ],
            options={
                'verbose_name': 'Article comment like',
                'verbose_name_plural': 'Article comment likes',
                'ordering': ('id',),
            },
        ),
    ]
