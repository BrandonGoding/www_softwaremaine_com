# Generated by Django 5.1.3 on 2024-11-22 12:11

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_remove_film_imdb_link_remove_film_youtube_link_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogrollpage",
            name="blog_description",
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]