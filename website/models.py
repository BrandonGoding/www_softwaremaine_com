from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import PageChooserBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page


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


class HomePage(Page):
    # Define the StreamField using your custom block
    content = StreamField(
        [
            ("hero", SimpleCenteredHeroWithBackgroundImageBlock()),
        ],
        blank=True,
    )

    # Define the content panels for the Wagtail admin interface
    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    # Prevent any subpages from being created under HomePage
    subpage_types = []
