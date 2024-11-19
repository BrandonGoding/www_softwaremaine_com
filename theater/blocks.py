from django.utils import timezone
from wagtail import blocks

from theater.models import Schedule


class NowPlayingBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    block_text = blocks.CharBlock()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["now_playing"] = Schedule.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now(),
            confirmed=True,
        )
        return context

    class Meta:
        label = "Now Playing"
        template = "theater/blocks/now_playing_block.html"
