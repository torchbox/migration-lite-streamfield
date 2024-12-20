from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from mlstreamfield.fields import StreamField


class BodyFieldMixin(models.Model):  # type: ignore[DJ008]
    body = StreamField(
        [
            ("text", blocks.TextBlock()),
            ("integer", blocks.IntegerBlock()),
            ("date", blocks.DateBlock()),
        ],
        blank=True,
    )

    class Meta:
        abstract = True


class TestPage(Page, BodyFieldMixin):
    content_panels = Page.content_panels + [FieldPanel("body")]

    def __str__(self):
        return self.title


@register_snippet
class TestSnippet(BodyFieldMixin, models.Model):
    title = models.CharField(max_length=255)
    panels = [FieldPanel("title"), FieldPanel("body")]

    def __str__(self):
        return self.title
