# Generated by Django 5.1.3 on 2024-11-17 19:13

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
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
                ("title", models.CharField(max_length=255)),
                (
                    "duration",
                    models.PositiveIntegerField(help_text="Duration in minutes"),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Theater",
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
                ("name", models.CharField(max_length=50)),
                ("capacity", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="theater.movie",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShowTime",
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
                ("start_time", models.DateTimeField()),
                ("is_sold_out", models.BooleanField(default=False)),
                (
                    "schedule",
                    modelcluster.fields.ParentalKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="showtimes",
                        to="theater.schedule",
                    ),
                ),
                (
                    "theater",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="showtimes",
                        to="theater.theater",
                    ),
                ),
            ],
            options={
                "ordering": ["start_time"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("theater", "start_time"),
                        name="unique_showtime_per_theater",
                    )
                ],
            },
        ),
    ]
