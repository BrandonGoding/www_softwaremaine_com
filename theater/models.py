from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet


@register_snippet
class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.CharField(
        max_length=10, blank=True, null=True, help_text="e.g., PG, R"
    )
    release_date = models.DateField(blank=True, null=True)
    poster = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )

    def __str__(self):
        return self.title

    panels = [
        FieldPanel("title"),
        FieldPanel("duration"),
        FieldPanel("description"),
        FieldPanel("rating"),
        FieldPanel("release_date"),
        FieldPanel("poster"),
    ]


@register_snippet
class Theater(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("capacity"),
    ]


@register_snippet
class Schedule(ClusterableModel):
    """
    A Schedule groups ShowTimes for a specific movie.
    """

    movie = models.ForeignKey(Film, on_delete=models.CASCADE, related_name="schedules")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Schedule for {self.movie.title} ({self.start_date} - {self.end_date})"

    panels = [
        FieldPanel("movie"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        InlinePanel("showtimes", label="ShowTimes"),
    ]


class ShowTime(models.Model):
    """
    Represents an individual showtime for a movie in a specific theater.
    """

    schedule = ParentalKey(
        Schedule, on_delete=models.CASCADE, related_name="showtimes", null=True
    )
    theater = models.ForeignKey(
        Theater, on_delete=models.SET_NULL, null=True, related_name="showtimes"
    )
    start_time = models.DateTimeField()
    is_sold_out = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["theater", "start_time"], name="unique_showtime_per_theater"
            )
        ]

    def __str__(self):
        return (
            f"{self.schedule.movie.title} in {self.theater.name} at {self.start_time}"
        )

    panels = [
        FieldPanel("theater"),
        FieldPanel("start_time"),
        FieldPanel("is_sold_out"),
    ]
