# Generated by Django 5.1.3 on 2024-11-22 22:02

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_blogcategory_blogpostpage_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="content",
            field=wagtail.fields.StreamField(
                [("hero", 11), ("now_playing", 13), ("recent_posts", 14)],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.CharBlock", (), {"required": True}),
                    1: ("wagtail.blocks.CharBlock", (), {"required": False}),
                    2: (
                        "wagtail.images.blocks.ImageChooserBlock",
                        (),
                        {"required": False},
                    ),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "Call-to-action text",
                            "required": False,
                            "verbose_name": "Call-to-action text",
                        },
                    ),
                    4: (
                        "wagtail.blocks.PageChooserBlock",
                        (),
                        {
                            "help_text": "Link to a page",
                            "required": False,
                            "verbose_name": "Call-to-action Page link",
                        },
                    ),
                    5: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("Read More", "Read More"),
                                ("Learn More", "Learn More"),
                            ],
                            "help_text": "Choose link text",
                            "required": False,
                            "verbose_name": "Call-to-action Link text",
                        },
                    ),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [[("cta_text", 3), ("cta_page_link", 4), ("cta_link_text", 5)]],
                        {"required": False},
                    ),
                    7: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"help_text": "", "required": False},
                    ),
                    8: ("wagtail.blocks.PageChooserBlock", (), {"required": False}),
                    9: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 7), ("page_link", 8)]],
                        {"label": "Primary Button", "required": False},
                    ),
                    10: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 7), ("page_link", 8)]],
                        {"label": "Secondary Button", "required": False},
                    ),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("header_text", 0),
                                ("sub_header_text", 1),
                                ("background_image", 2),
                                ("cta", 6),
                                ("primary_button", 9),
                                ("secondary_button", 10),
                            ]
                        ],
                        {},
                    ),
                    12: ("wagtail.blocks.CharBlock", (), {}),
                    13: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 12), ("block_text", 12)]],
                        {},
                    ),
                    14: ("wagtail.blocks.StructBlock", [[]], {}),
                },
            ),
        ),
    ]
