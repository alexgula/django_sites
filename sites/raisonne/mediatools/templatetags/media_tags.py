# coding=utf-8
import urlparse, os

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from uuid import uuid4
from django.template.defaultfilters import stringfilter
from django.template.base import FilterExpression

register = template.Library()


class DziNode(template.Node):
    def __init__(self, var_name):
        self.var = template.Variable(var_name)

    def render(self, context):
        url = self.var.resolve(context)
        return render_to_string('dzi.html', {'url': url, 'container_id': str(uuid4())})

def do_dzi(parser, token):
    bits = token.split_contents()
    if len(bits) == 2:
        var_name = bits[1]
    else:
        raise template.TemplateSyntaxError(u"Syntax is: {0} variable,\
 where variable should return url to DeepZoom descriptor".format(bits[0]))
    return DziNode(var_name)

register.tag('dzi', do_dzi)


class ImageNode(template.Node):
    def __init__(self, image_field, title_field, content_url, content_root):
        self.image_field = image_field
        self.title_field = title_field
        self.content_url = content_url
        self.content_root = content_root

    def render(self, context):
        image = _media(self.image_field.resolve(context), self.content_url, self.content_root)
        title = self.title_field.resolve(context)
        return u"<img src='{image}' alt='{title}' title='{title}'></img>".format(image=image, title=title)

def _do_image(parser, token, content_url, content_root):
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

    image_field = FilterExpression(image_field_name, parser)
    title_field = FilterExpression(title_field_name, parser)
    return ImageNode(image_field, title_field, content_url, content_root)

def do_image(parser, token):
    return _do_image(parser, token, settings.MEDIA_URL, settings.MEDIA_ROOT)

def do_staticimage(parser, token):
    return _do_image(parser, token, settings.STATIC_URL, settings.STATIC_ROOT)

register.tag('image', do_image)
register.tag('staticimage', do_staticimage)


def _absolute_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    domain = Site.objects.get_current().domain
    return 'http://%s%s' % (domain, url)


def _media(filename, content_url, content_root, flags=set()):
    url = urlparse.urljoin(content_url, filename)
    if 'absolute' in flags:
        url = _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or 'timestamp' in flags:
        fullname = os.path.join(content_root, *filename.split('/'))
        if os.path.exists(fullname):
            url += '?%d' % os.path.getmtime(fullname)
    return url


@register.simple_tag
def media(filename, flags=''):
    flags = set(f.strip() for f in flags.split(','))
    return _media(filename, settings.MEDIA_URL, settings.MEDIA_ROOT, flags)


@register.simple_tag
def staticmedia(filename, flags=''):
    flags = set(f.strip() for f in flags.split(','))
    return _media(filename, settings.STATIC_URL, settings.STATIC_ROOT, flags)


@register.filter
@stringfilter
def format(value, arg):
    try:
        return value.format(arg)
    except:
        return value
