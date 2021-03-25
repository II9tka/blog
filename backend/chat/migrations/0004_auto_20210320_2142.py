# Generated by Django 2.2 on 2021-03-20 21:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_auto_20210320_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='chats', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='participants',
            field=models.ManyToManyField(related_name='chat_groups', to=settings.AUTH_USER_MODEL, verbose_name='Participants'),
        ),
    ]