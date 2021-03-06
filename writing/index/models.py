from django.db import models
from django.utils import timezone
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock

from .tags import StoryMainTags, ChapterTags, ArticleTags
from .categories import ContentCategory


## BLOG / ARTICLE MODELS

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        articles = self.get_children().live()
        context['articles'] = articles
        return context


class BlogArticlePage(Page):
    tagline = RichTextField(blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    body = StreamField([
        ('intro', blocks.RichTextBlock()),
        ('textblock', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ])
    tags = ClusterTaggableManager(through=ArticleTags, blank=True)
    categories = ParentalManyToManyField('index.ContentCategory', blank=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('body'),
        index.FilterField('published_date'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('published_date'),
            FieldPanel('tags'),
            FieldPanel('categories'),
            ]),
        FieldPanel('tagline'),
        StreamFieldPanel('body'),
        InlinePanel('article_images', label="Article images"),
    ]


## STORY MODELS

# PAGE MODELS
class StoryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    subpage_types = ['index.StoryMainPage']

    def get_context(self, request):
        context = super().get_context(request)
        stories = self.get_children().live().order_by('-last_published_at')
        context['stories'] = stories

        return context

    class Meta:
        verbose_name = 'Story Index Page'


class StoryMainPage(Page):
    published_date = models.DateTimeField(default=timezone.now)
    synopsis = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=StoryMainTags, blank=True)
    categories = ParentalManyToManyField('index.ContentCategory', blank=True)

    search_fields = [
        index.SearchField('title'),
        index.SearchField('synopsis'),
        index.FilterField('published_date'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('published_date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
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
        verbose_name = 'Story Main Page'


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
        verbose_name = 'Chapter Page'


# TAG INDEX PAGE
class TagIndexPage(Page):

    def get_context(self, request):
        # Get tagged items
        tag = request.GET.get('tag')

        # Chapters & Stories Seperately
        chapters = ChapterPage.objects.filter(tags__name=tag)
        stories = StoryMainPage.objects.filter(tags__name=tag)
        articles = BlogArticlePage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['content_types'] = [('Stories', stories),
                                    ('Chapters', chapters),
                                    ('Articles', articles)]
        context['meta'] = tag

        return context


# Cetegory index page
class CategoryIndexPage(Page):

    def get_context(self, request):
        # get category
        category = request.GET.get('category')

        stories = StoryMainPage.objects.filter(categories__name=category)
        articles = BlogArticlePage.objects.filter(categories__name=category)
        category_info = ContentCategory.objects.filter(name=category)

        context = super().get_context(request)
        context['content_types'] = [('Stories', stories),
                                    ('Articles', articles)]
        context['meta'] = category

        try:
            context['info'] = category_info[0]
        except IndexError:
            context['info'] = None

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


class ArticleGalleryImage(Orderable):
    article = ParentalKey(BlogArticlePage, on_delete=models.CASCADE,
                        related_name='article_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE,
                              related_name='+')
    caption = models.CharField(blank=True, max_length=200)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
