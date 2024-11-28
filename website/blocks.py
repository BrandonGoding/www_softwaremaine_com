from collections import defaultdict

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import localtime
from wagtail import blocks
from wagtail.blocks import PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class CallToActionTextChoices(blocks.ChoiceBlock):
    choices = [
        ("Read More", "Read More"),
        ("Learn More", "Learn More"),
    ]


class CallToAction(blocks.StructBlock):
    cta_text = blocks.CharBlock(
        required=False,
        help_text="Call-to-action text",
        verbose_name="Call-to-action text",
    )
    cta_page_link = PageChooserBlock(
        required=False,
        help_text="Link to a page",
        verbose_name="Call-to-action Page link",
    )
    cta_link_text = CallToActionTextChoices(
        required=False,
        help_text="Choose link text",
        verbose_name="Call-to-action Link text",
    )

    def clean(self, value):
        # Call the parent clean method to retain base validation
        cleaned_data = super().clean(value)

        cta_text = cleaned_data.get("cta_text")
        cta_page_link = cleaned_data.get("cta_page_link")
        cta_link_text = cleaned_data.get("cta_link_text")

        # Check if any field is filled
        filled_fields = [bool(cta_text), bool(cta_page_link), bool(cta_link_text)]
        if any(filled_fields) and not all(filled_fields):
            raise ValidationError(
                "All fields ('cta_text', 'cta_page_link', and 'cta_link_text') must be"
                " filled if any one is provided."
            )

        return cleaned_data

    class Meta:
        icon = "link"
        label = "Call to Action"


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=False, help_text="")
    page_link = PageChooserBlock(required=False)

    def clean(self, value):
        # Call the parent clean method to retain base validation
        cleaned_data = super().clean(value)

        text = cleaned_data.get("text")
        page_link = cleaned_data.get("page_link")

        # Custom validation: if one is filled, both must be filled
        if (text and not page_link) or (page_link and not text):
            raise ValidationError(
                "Both 'text' and 'page_link' must be filled out if one is provided."
            )

        return cleaned_data

    class Meta:
        icon = "link"
        label = "Button"


class SimpleCenteredHeroWithBackgroundImageBlock(blocks.StructBlock):
    header_text = blocks.CharBlock(required=True)
    sub_header_text = blocks.CharBlock(required=False)
    background_image = ImageChooserBlock(required=False)
    cta = CallToAction(required=False)
    primary_button = ButtonBlock(required=False, label="Primary Button")
    secondary_button = ButtonBlock(required=False, label="Secondary Button")

    class Meta:
        icon = "placeholder"
        label = "Simple Centered Hero"
        template = "website/blocks/simple_centered_hero.html"


class NowPlayingBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    block_text = blocks.CharBlock()

    def get_context(self, request, *args, **kwargs):
        from website.models import Schedule

        context = super().get_context(request, *args, **kwargs)
        current_time = timezone.now()

        now_playing = Schedule.objects.filter(
            start_date__lte=current_time,
            end_date__gte=current_time,
            confirmed=True,
        )

        grouped_showtimes = []
        for schedule in now_playing:
            showtimes = defaultdict(list)
            for showtime in schedule.showtimes.filter(start_time__gte=current_time):
                local_start_time = localtime(showtime.start_time)
                showtimes[local_start_time.date()].append(local_start_time.time())
            grouped_showtimes.append(
                {
                    "movie": schedule.movie,
                    "showtimes_by_date": dict(showtimes),
                    "next_showtime": schedule.next_showtime,
                }
            )

        context["now_playing"] = grouped_showtimes
        return context

    class Meta:
        label = "Now Playing"
        template = "website/blocks/now_playing_block.html"


class RecentPostsBlock(blocks.StructBlock):

    def get_context(self, request, *args, **kwargs):
        from website.models import BlogPostPage

        context = super().get_context(request, *args, **kwargs)
        context["most_recent_posts"] = BlogPostPage.objects.live().order_by(
            "-published_date"
        )[:3]
        return context

    class Meta:
        label = "Recent Posts"
        template = "website/blocks/recent_posts_block.html"
