# Generated by Django 5.1.3 on 2024-11-20 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="film",
            name="imdb_link",
        ),
        migrations.RemoveField(
            model_name="film",
            name="youtube_link",
        ),
        migrations.AddField(
            model_name="film",
            name="imdb_id",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="film",
            name="youtube_id",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
