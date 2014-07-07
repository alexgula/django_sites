# coding=utf-8
import urlparse, os

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import stringfilter
from django.template.base import FilterExpression

register = template.Library()


class ImageNode(template.Node):
    def __init__(self, image_field, title_field):
        self.image_field = image_field
        self.title_field = title_field

    def render(self, context):
        image = urlparse.urljoin(settings.MEDIA_URL, self.image_field.resolve(context))
        title = self.title_field.resolve(context)
        return u"<img src='{image}' alt='{title}' title='{title}'></img>".format(image=image, title=title)

def do_image(parser, token):
    bits = token.split_contents()

    def get_bit(idx, default = None):
        if len(bits) > idx:
            return bits[idx]
        else:
            return default

    image_field_name = get_bit(1)

    if image_field_name[0] not in "\"'":
        default_title = image_field_name.rsplit('.',2)[0] + '.name'
    else:
        default_title = None
    title_field_name = get_bit(2, default_title)

    if not (image_field_name and title_field_name):
        raise template.TemplateSyntaxError("Syntax is: {0} image title".format(bits[0]))

    # run filters, for example - format image reference or title
    image_field = FilterExpression(image_field_name, parser)
    title_field = FilterExpression(title_field_name, parser)
    return ImageNode(image_field, title_field)

register.tag('image', do_image)

@register.filter
@stringfilter
def format(value, arg):
    try:
        return value.format(arg)
    except:
        return value
