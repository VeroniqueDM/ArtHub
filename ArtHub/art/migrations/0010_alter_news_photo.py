# Generated by Django 4.0.4 on 2022-04-27 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0009_alter_event_date_alter_event_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.URLField(verbose_name='Photo URL'),
        ),
    ]
