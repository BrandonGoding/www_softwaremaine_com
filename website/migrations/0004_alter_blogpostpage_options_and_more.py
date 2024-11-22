# Generated by Django 5.1.3 on 2024-11-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_alter_blogrollpage_blog_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpostpage",
            options={
                "ordering": ["-published_date"],
                "verbose_name": "Blog Post",
                "verbose_name_plural": "Blog Posts",
            },
        ),
        migrations.AlterField(
            model_name="blogrollpage",
            name="blog_description",
            field=models.TextField(blank=True),
        ),
    ]