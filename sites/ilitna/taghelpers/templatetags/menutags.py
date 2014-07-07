# coding=utf-8
from django import template

register = template.Library()

FIGURE_TEMPLATE = u"""
<span class='figure-left'></span>
<span class='figure-tile'>{}</span>
<span class='figure-right'></span>
"""

@register.tag(name='figure')
def do_figure(parser, token):
    nodelist = parser.parse(('endfigure',))
    parser.delete_first_token()
    return FigureNode(nodelist)


class FigureNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return FIGURE_TEMPLATE.format(output)
