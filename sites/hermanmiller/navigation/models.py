# coding=utf-8
from django.db import models
from django.core import urlresolvers


class BaseNavigationNode(object):

    def __init__(self, name):
        self.name = name


class NavigationNode(BaseNavigationNode):

    def __init__(self, name, url):
        super(NavigationNode, self).__init__(name)
        self.url = url

    def __repr__(self):
        return u"{} - {}".format(self.name, self.url)


class StaticNode(BaseNavigationNode):

    def __init__(self, name, viewname, *args, **kwargs):
        super(StaticNode, self).__init__(name)
        self.viewname = viewname
        self.args = args
        self.kwargs = kwargs

    @property
    def url(self):
        return urlresolvers.reverse(self.viewname, *self.args, **self.kwargs)


class ModelNode(BaseNavigationNode):

    def __init__(self, obj):
        super(ModelNode, self).__init__(obj.__unicode__())
        self.object = obj

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

    @staticmethod
    def nav_node(obj):
        """Generate ModelNode from Django models, just for convenience."""
        return ModelNode(obj) if isinstance(obj, models.Model) else obj

    def is_active(self, url):
        if type(url) == set:
            return not self.url_cache.isdisjoint(url)
        return url in self.url_cache

    def is_active_leaf(self, url):
        if len(self.nodes) > 0:
            return url == self.nodes[-1].url
        else:
            return False

    def repr_active(self, url):
        result = []
        if self.is_active(url):
            result.append('active')
        if self.is_active_leaf(url):
            result.append('active-leaf')
        return ' '.join(result)

    def __repr__(self):
        nodes = u", ".join([unicode(node) for node in self.nodes])
        url_cache = u", ".join(self.url_cache)
        return u"nodes = {} |||| urls = {}".format(nodes, url_cache)
