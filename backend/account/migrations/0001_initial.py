# Generated by Django 3.1.7 on 2021-04-06 19:17

import backend.account.models.account_connection_history_model
import backend.account.models.account_model
import colorfield.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('filer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('status_type', enumfields.fields.EnumIntegerField(default=1, enum=backend.account.models.account_model.AccountPrivacyStatus, help_text='Account publicity status.', verbose_name='Status type')),
                ('gender', enumfields.fields.EnumIntegerField(default=0, enum=backend.account.models.account_model.AccountGender, verbose_name='Gender')),
                ('background_color', colorfield.fields.ColorField(default='#FFFFFF', help_text='User can customize background color of the account. \nDefault color is White (#FFFFFF)', max_length=18, verbose_name='Background color')),
                ('city', models.CharField(blank=True, default='', help_text="User's hometown name. Max length is 100.", max_length=100, verbose_name='City')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone')),
                ('workplace', models.CharField(blank=True, default='', help_text="User's workplace. Max length is 150.", max_length=150, verbose_name='Workplace')),
                ('work_experience', models.TextField(blank=True, default='', help_text='User can specify work experience. Max length is 2000.', max_length=2000, verbose_name='Work experience')),
                ('about', models.TextField(blank=True, default='', help_text='User information about myself. Max length is 2000.', max_length=2000, verbose_name='About')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'ordering': ('id',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AccountImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL, verbose_name='Account')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filer.image', verbose_name='Image')),
            ],
            options={
                'verbose_name': 'Account avatar',
                'verbose_name_plural': 'Accounts avatar',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='AccountConnectionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100, verbose_name='Session ID')),
                ('connection_status', enumfields.fields.EnumIntegerField(default=0, enum=backend.account.models.account_connection_history_model.ConnectionStatus, help_text='Account connection status.', verbose_name='Connection status')),
                ('last_connection', models.DateTimeField(auto_now=True, verbose_name='Last connection')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to=settings.AUTH_USER_MODEL, verbose_name='account')),
            ],
            options={
                'unique_together': {('account', 'session_id')},
            },
        ),
    ]
