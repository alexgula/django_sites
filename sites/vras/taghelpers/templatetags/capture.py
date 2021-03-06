# coding=utf-8
"""https://github.com/nathanborror/django-basic-apps/blob/01b37fb28605504893811ffac89cb97852f2e0a4/basic/tools/templatetags/capture.py

Tags like url and trans provide no way to get the result as a context variable. But how would you get a computed URL into a blocktrans?

This snippet solves the general problem. Just put the template code whose output you want to capture within captureas tags. For example:

{% capture as login_url %}{% url login %}{% endcapture %}
{% blocktrans %}
<a href="{{login_url}}">login</a>
{%endblocktrans%}
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.tag
def capture(parser, token):
    """{% capture as [foo] %}"""
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'capture' node requires `as (variable name)`.")
    nodelist = parser.parse(('endcapture',))
    parser.delete_first_token()
    return CaptureNode(nodelist, bits[2])


class CaptureNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = mark_safe(output.strip())
        return ''
