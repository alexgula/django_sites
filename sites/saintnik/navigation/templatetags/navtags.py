# coding=utf-8
from django.conf import settings
from django import template
from django.template.base import TemplateSyntaxError, Node
from django.template.defaulttags import kwarg_re
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse, NoReverseMatch
from ..models import Trail

register = template.Library()

def link_repr(obj):
    return u"<a href='{url}'>{name}</a>".format(url=obj.url, name=obj.name)


class ActiveURLNode(Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        view_name = self.view_name
        view_name = view_name.resolve(context)

        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = reverse(view_name, args=args, kwargs=kwargs, current_app=context.current_app)
        except NoReverseMatch, e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse(project_name + '.' + view_name,
                              args=args, kwargs=kwargs,
                              current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        trail = context.get('trail')
        if not trail:
            trail = Trail()
        repr = trail.repr_active(url)

        if self.asvar:
            context[self.asvar] = repr
            return ''
        else:
            return repr


class ActiveModelNode(Node):
    def __init__(self, object_name, asvar):
        self.object_name = object_name
        self.asvar = asvar

    def render(self, context):
        obj = self.object_name.resolve(context)
        url = obj.get_absolute_url()

        trail = context.get('trail')
        if not trail:
            trail = Trail()
        repr = trail.repr_active(url)

        if self.asvar:
            context[self.asvar] = repr
            return ''
        else:
            return repr

@register.simple_tag(takes_context=True)
def breadcrumbs(context, delimiter=u" - "):
    nodes = context.get('trail', Trail()).nodes

    if len(nodes) > 0:
        # Nodes representation in reverse order
        nodes_repr = [link_repr(node) for node in nodes[:-1]] + [unicode(nodes[-1].name)]
        return delimiter.join(nodes_repr)
    return u""

@register.tag
def active_url(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return ActiveURLNode(viewname, args, kwargs, asvar)

@register.tag
def active_model(parser, token):
    bits = token.split_contents()
    if len(bits) != 2 and len(bits) != 4:
        raise TemplateSyntaxError("'%s' takes exactly one argument"
                                  " (Model object)" % bits[0])
    object_name = parser.compile_filter(bits[1])
    if len(bits) == 4 and bits[-2] == 'as':
        asvar = bits[-1]
    else:
        asvar = None

    return ActiveModelNode(object_name, asvar)
