# Generated by Django 4.0.4 on 2022-04-26 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_artist_artmoduser_regularuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularprofile',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
