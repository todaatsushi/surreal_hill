from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


# PAGE MODELS
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

    class Meta:
        verbose_name = 'indexpage'


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
        InlinePanel('story_images', label="Story images"),
    ]

    parent_page_types = ['index.StoryIndexPage']
    subpage_types = ['index.ChapterPage']

    def get_context(self, request):
        context = super().get_context(request)
        chapters = self.get_children().live()
        context['chapters'] = chapters
        return context

    class Meta:
        verbose_name = 'storypage'


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
        InlinePanel('chapter_images', label="Chapter images"),
    ]

    class Meta:
        verbose_name = 'chapterpage'


# IMAGE MODEL
class StoryMainPageGalleryImage(Orderable):
    story = ParentalKey(StoryMainPage, on_delete=models.CASCADE,
                        related_name='story_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE,
                              related_name='+')
    caption = models.CharField(blank=True, max_length=200)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class ChapterPageGalleryImage(Orderable):
    story = ParentalKey(ChapterPage, on_delete=models.CASCADE,
                        related_name='chapter_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE,
                              related_name='+')
    caption = models.CharField(blank=True, max_length=200)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
