# Generated by Django 2.2 on 2021-03-03 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('cover', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='filer.Image', verbose_name='Cover')),
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
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='article.Article', verbose_name='Article')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filer.Image', verbose_name='Article image')),
            ],
            options={
                'verbose_name': 'Article Image',
                'verbose_name_plural': 'Article Images',
                'ordering': ('id',),
            },
        ),
    ]