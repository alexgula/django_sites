# coding=utf-8
from django.db import models
from django.core import urlresolvers


class NavigationNode(object):

    def __repr__(self):
        return u"{} - {}".format(self.name, self.url)


class StaticNode(NavigationNode):

    def __init__(self, name, viewname, *args, **kwargs):
        self.name = name
        self.viewname = viewname
        self.args = args
        self.kwargs = kwargs

    @property
    def url(self):
        return urlresolvers.reverse(self.viewname, *self.args, **self.kwargs)


class ModelNode(NavigationNode):

    def __init__(self, obj):
        self.object = obj
        self.name = self.object.__unicode__()

    @property
    def url(self):
        return self.object.get_absolute_url()


class Trail(object):

    def __init__(self, *args):
        """Initialize trail by list of objects, starting from the current object up to its parents.

        Can also accept iterables, in which case will iterate over items of an iterable."""
        self.nodes = []
        self._url_cache = None

        for obj in args:
            if hasattr(obj, '__iter__'):
                for item in obj:
                    node = self.nav_node(item)
                    self.nodes.append(node)
            else:
                node = self.nav_node(obj)
                self.nodes.append(node)

    @property
    def url_cache(self):
        """Lazy property, otherwise localeurl is not initialized."""
        if self._url_cache is None:
            self._url_cache = set()
            for node in self.nodes:
                self._url_cache.add(node.url)
        return self._url_cache

    @classmethod
    def nav_node(cls, obj):
        """Generate ModelNode from Django models, just for convenience."""
        return ModelNode(obj) if isinstance(obj, models.Model) else obj

    def is_active(self, url):
        if type(url) == set:
            return not self.url_cache.isdisjoint(url)
        return url in self.url_cache

    def repr_active(self, url):
        return 'active' if self.is_active(url) else ''

    def __repr__(self):
        nodes = u", ".join([unicode(node) for node in self.nodes])
        url_cache = u", ".join(self.url_cache)
        return u"nodes = {} |||| urls = {}".format(nodes, url_cache)


try:
    from mptt.models import MPTTModel

    class MPTTTrail(Trail):

        def __init__(self, *args):
            """Initialize trail by list of objects, starting from the current object up to its parents."""
            super(MPTTTrail, self).__init__(*args)

            # For each MPTT node in trail add its ancestors to the cache
            for node in self.nodes:
                if isinstance(node, ModelNode) and isinstance(node.object, MPTTModel):
                    for ancestor in node.object.get_ancestors():
                        self.url_cache.add(ancestor.get_absolute_url())
except ImportError:
    pass
