# coding=utf-8
from django import template
from picassoft.utils.templatetags.markup import restructuredtext

from ..models import TextBlock

register = template.Library()

def get_block_text(context, block_code):
    request = context.get('request', {}) # In case if request absence just ignore this fact
    if not hasattr(request, 'text_blocks'):
        request.text_blocks = {block.code: block for block in TextBlock.objects.all()}
    text_block = request.text_blocks.get(block_code)
    return text_block.text if text_block else u""

@register.simple_tag(takes_context=True)
def text_block(context, block_code):
    return get_block_text(context, block_code)

@register.simple_tag(takes_context=True)
def rst_block(context, block_code):
    return restructuredtext(get_block_text(context, block_code))
