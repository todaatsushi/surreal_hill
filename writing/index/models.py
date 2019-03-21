from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index


class StoryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    subpage_types = ['index.StoryMainPage']


class StoryMainPage(Page):
    published_date = models.DateTimeField(default=timezone.now)
    synopsis = RichTextField(blank=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('synopsis'),
        index.FilterField('published_date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('synopsis', classname='full'),
    ]

    parent_page_types = ['index.StoryIndexPage']
    subpage_types = ['index.ChapterPage']


class ChapterPage(Page):
    published_date = models.DateTimeField(default=timezone.now)
    order = models.IntegerField(null=True)
    body = RichTextField(blank=True)
    story = models.ForeignKey(StoryMainPage, on_delete=models.SET_NULL, null=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('order'),
        index.SearchField('body'),
        index.FilterField('published_date'),
    ]
