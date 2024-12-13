from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.images.models import Image
from wagtail.models import Orderable, Page, Site
from wagtail.snippets.models import register_snippet

from website.blocks import (
    ComingSoonBlock,
    NowPlayingBlock,
    RecentPostsBlock,
    SimpleCenteredHeroWithBackgroundImageBlock,
)
from website.services import omdb_service


class HomePage(Page):
    # Define the StreamField using your custom block
    content = StreamField(
        [
            ("hero", SimpleCenteredHeroWithBackgroundImageBlock()),
            ("coming_soon", ComingSoonBlock()),
            ("now_playing", NowPlayingBlock()),
            ("recent_posts", RecentPostsBlock()),
        ],
        blank=True,
    )

    # Define the content panels for the Wagtail admin interface
    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    # Prevent any subpages from being created under HomePage
    subpage_types = ["website.BlogRollPage", "website.FilmArchivePage"]


class FilmArchivePage(Page):
    parent_page_types = ["website.HomePage"]
    subpage_types = ["website.Film"]


@register_snippet
class BlogAuthor(models.Model):
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    avatar = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.last_name + ", " + self.first_name

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name", "first_name")


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=25)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    panels = [
        FieldPanel("name"),
        FieldPanel("site"),
    ]

    def __str__(self):
        return self.name


class BlogRollPage(Page):
    max_count = 1
    blog_description = models.TextField(blank=True)

    parent_page_types = ["website.HomePage"]
    subpage_types = ["website.BlogPostPage"]

    content_panels = Page.content_panels + [
        FieldPanel("blog_description"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = (
            BlogPostPage.objects.child_of(self).order_by("-published_date").live()
        )
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 6)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)
        context["blog_posts"] = posts
        context["start_index"] = posts.start_index()
        context["end_index"] = posts.end_index()
        context["total_posts"] = all_posts.count()
        return context


class BlogPostPage(Page):
    author = models.ForeignKey(
        BlogAuthor, on_delete=models.PROTECT, related_name="posts"
    )
    subject_film = models.ForeignKey(
        to="website.Film",
        on_delete=models.PROTECT,
        related_name="reviews",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        to="website.BlogCategory", on_delete=models.SET_NULL, null=True, blank=True
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
        FieldPanel("subject_film"),
        FieldPanel("category"),
        FieldPanel("published_date"),
        FieldPanel("banner_image"),
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["recent_posts"] = (
            BlogPostPage.objects.child_of(self.get_parent())
            .exclude(id=self.id)
            .order_by("-published_date")
            .live()[:3]
        )
        context["now_playing"] = Schedule.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            confirmed=True,
        )
        return context

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-published_date"]


class ProductionStill(Orderable):
    page = ParentalKey(
        "website.Film", on_delete=models.CASCADE, related_name="production_stills"
    )
    image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )


class Film(Page):
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.CharField(
        max_length=10, blank=True, null=True, help_text="e.g., PG, R"
    )
    release_date = models.DateField(blank=True, null=True)
    poster = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )
    banner_image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name="+", blank=True, null=True
    )
    imdb_id = models.CharField(max_length=15, null=True, blank=True)
    youtube_id = models.CharField(max_length=15, null=True, blank=True)
    omdb_json = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title

    content_panels = Page.content_panels + [
        FieldPanel("duration"),
        FieldPanel("description"),
        FieldPanel("rating"),
        FieldPanel("release_date"),
        FieldPanel("poster"),
        FieldPanel("banner_image"),
        MultiFieldPanel(
            [
                FieldPanel("imdb_id"),
                FieldPanel("youtube_id"),
                FieldPanel("omdb_json"),
            ],
            heading="External Keys",
        ),
        InlinePanel("production_stills", label="Production Still"),
    ]

    schedule_content_panels = [InlinePanel("schedules", label="Schedule")]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(schedule_content_panels, heading="Schedules"),
            ObjectList(Page.promote_panels, heading="Promote"),
        ]
    )

    def save(self, *args, **kwargs):
        if self.omdb_json is None and self.imdb_id:
            try:
                imdb_data = omdb_service.get_movie_data_from_imdb(self.imdb_id)
            except Exception as e:
                print(e)
                imdb_data = None
            self.omdb_json = imdb_data
        super(Film, self).save(*args, **kwargs)


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


class Schedule(ClusterableModel):
    """
    A Schedule groups ShowTimes for a specific movie.
    """

    movie = ParentalKey(
        "website.Film", on_delete=models.CASCADE, related_name="schedules"
    )
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
    start_time = models.DateTimeField()
    is_sold_out = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.schedule.movie.title} at {self.start_time}"

    panels = [
        FieldPanel("start_time"),
        FieldPanel("is_sold_out"),
        FieldPanel("cancelled"),
    ]
