from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField


@register_snippet
class ContentCategory(models.Model):
    name = models.CharField(max_length=75)
    one_line = models.CharField(max_length=100, default="")
    about = RichTextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('one_line'),
        FieldPanel('about'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Content Category'
