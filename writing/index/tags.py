from django.db import models

from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

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


class ArticleTags(TaggedItemBase):
    content_object = ParentalKey(
        'BlogArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
