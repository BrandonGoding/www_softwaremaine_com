# Generated by Django 5.1.3 on 2024-11-22 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
        ("website", "0004_alter_blogpostpage_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=25)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="blogpostpage",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="website.blogcategory",
            ),
        ),
    ]