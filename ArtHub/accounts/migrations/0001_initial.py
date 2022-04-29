# Generated by Django 4.0.4 on 2022-04-29 19:10

import ArtHub.common.validators
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtHubUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=25, unique=True)),
                ('type', models.CharField(choices=[('ARTIST', 'Artist'), ('REGULAR_USER', 'Regular User'), ('ART_MOD', 'Art Mod')], max_length=50)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2), ArtHub.common.validators.validate_only_letters_or_space])),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2), ArtHub.common.validators.validate_only_letters_or_space])),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('date_of_birth', models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.TextField()),
                ('website', models.URLField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.arthubuser',),
        ),
        migrations.CreateModel(
            name='ArtModUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.arthubuser',),
        ),
        migrations.CreateModel(
            name='RegularUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.arthubuser',),
        ),
    ]
