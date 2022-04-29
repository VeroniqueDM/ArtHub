# Generated by Django 4.0.4 on 2022-04-28 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('art', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artpiece',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserNewsTimestamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, null=True, verbose_name='TTime Stamp')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timestamps', to='art.news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timestamps', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
