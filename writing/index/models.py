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

    def get_context(self, request):
        context = super().get_context(request)
        stories = self.get_children().live()
        context['stories'] = stories
        return context


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

    def get_context(self, request):
        context = super().get_context(request)
        chapters = self.get_children().live()
        context['chapters'] = chapters
        return context


class ChapterPage(Page):
    published_date = models.DateTimeField(default=timezone.now)
    order = models.IntegerField(null=True)
    body = RichTextField(blank=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('order'),
        index.SearchField('body'),
        index.FilterField('published_date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('order'),
        FieldPanel('body', classname='full'),
    ]
