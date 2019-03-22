from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    tagline = RichTextField(blank=True)
    body = StreamField([
        ('welcome', blocks.RichTextBlock()),
        ('about', blocks.RichTextBlock()),
        ('photo', ImageChooserBlock()),
        ])

    content_panels = Page.content_panels + [
        FieldPanel('tagline', classname='full'),
        StreamFieldPanel('body')
    ]
