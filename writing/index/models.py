from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


# TAG MODELS
class StoryMainTags(TaggedItemBase):
    content_object = ParentalKey(
        'StoryMainPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ChapterTags(TaggedItemBase):
    content_object = ParentalKey(
        'ChapterPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


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
    tags = ClusterTaggableManager(through=StoryMainTags, blank=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('synopsis'),
        index.FilterField('published_date'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('published_date'),
            FieldPanel('tags')
        ], heading='Meta Information'),
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
    tags = ClusterTaggableManager(through=ChapterTags, blank=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('order'),
        index.SearchField('body'),
        index.FilterField('published_date'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('published_date'),
            FieldPanel('tags')
        ], heading='Meta Information'),
        FieldPanel('order'),
        FieldPanel('body', classname='full'),
        InlinePanel('chapter_images', label="Chapter images"),
    ]

    class Meta:
        verbose_name = 'chapterpage'


# TAG INDEX PAGE
class TagIndexPage(Page):

    def get_context(self, request):
        # Get tagged items
        tag = request.GET.get('tag')

        # Chapters & Stories Seperately
        chapters = ChapterPage.objects.filter(tags__name=tag)
        stories = StoryMainPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['chapters'] = chapters
        context['stories'] = stories
        return context


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
