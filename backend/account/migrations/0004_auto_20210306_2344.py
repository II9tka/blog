# Generated by Django 2.2.8 on 2021-03-06 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210305_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]
