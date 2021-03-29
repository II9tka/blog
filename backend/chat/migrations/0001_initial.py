# Generated by Django 3.1.7 on 2021-03-29 23:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='chats', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('participants', models.ManyToManyField(blank=True, related_name='chat_groups', to=settings.AUTH_USER_MODEL, verbose_name='Participants')),
            ],
            options={
                'verbose_name': 'Chat Group',
                'verbose_name_plural': 'Chat groups',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Message creation time.', verbose_name='Timestamp')),
                ('text', models.TextField(max_length=2000, verbose_name='Text')),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chat', verbose_name='Chat room')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
