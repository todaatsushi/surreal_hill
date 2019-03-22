from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel


@register_snippet
class ContentCategory(models.Model):
    name = models.CharField(max_length=75)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'story_category'
