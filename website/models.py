from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.models import Image
from wagtail.models import Page, Site
from wagtail.snippets.models import register_snippet

from website.blocks import NowPlayingBlock, SimpleCenteredHeroWithBackgroundImageBlock


class HomePage(Page):
    # Define the StreamField using your custom block
    content = StreamField(
        [
            ("hero", SimpleCenteredHeroWithBackgroundImageBlock()),
            ("now_playing", NowPlayingBlock()),
        ],
        blank=True,
    )

    # Define the content panels for the Wagtail admin interface
    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    # Prevent any subpages from being created under HomePage
    subpage_types = ["website.BlogRollPage"]


@register_snippet
class BlogAuthor(models.Model):
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.last_name + ", " + self.first_name

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name", "first_name")


class BlogRollPage(Page):
    max_count = 1
    blog_description = models.CharField(max_length=255)

    parent_page_types = ["website.HomePage"]
    subpage_types = ["website.BlogPostPage"]

    content_panels = Page.content_panels + [
        FieldPanel("blog_description"),
    ]


class BlogPostPage(Page):
    author = models.ForeignKey(
        BlogAuthor, on_delete=models.PROTECT, related_name="posts"
    )
    body = RichTextField()
    published_date = models.DateField(blank=True, null=True)
    banner_image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )

    parent_page_types = ["website.BlogRollPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("published_date"),
        FieldPanel("banner_image"),
        FieldPanel("body"),
    ]


class MovieReviewPost(BlogPostPage):
    movie = models.ForeignKey(
        to="website.Film", on_delete=models.PROTECT, related_name="reviews"
    )


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
    imdb_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    panels = [
        FieldPanel("title"),
        FieldPanel("duration"),
        FieldPanel("description"),
        FieldPanel("rating"),
        FieldPanel("release_date"),
        FieldPanel("poster"),
        MultiFieldPanel(
            [
                FieldPanel("imdb_link"),
                FieldPanel("youtube_link"),
            ],
            heading="External Links",
        ),
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
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for {self.movie.title} ({self.start_date} - {self.end_date})"

    panels = [
        FieldPanel("movie"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("confirmed"),
        InlinePanel("showtimes", label="ShowTimes"),
    ]

    @property
    def next_showtime(self):
        next_scheduled = (
            self.showtimes.filter(start_time__gte=timezone.now())
            .order_by("start_time")
            .first()
        )
        return next_scheduled.start_time if next_scheduled else None


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
    cancelled = models.BooleanField(default=False)

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
        FieldPanel("cancelled"),
    ]
