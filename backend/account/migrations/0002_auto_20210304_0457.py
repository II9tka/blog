# Generated by Django 2.2.8 on 2021-03-04 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='phone',
            new_name='phone_number',
        ),
    ]