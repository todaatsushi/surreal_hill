from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    header = models.CharField(max_length=50, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('title', classname='full'),
        FieldPanel('header', classname='full'),
        FieldPanel('body', classname='full'),
    ]
