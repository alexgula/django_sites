# coding=utf-8
import six
import collections


def tabulate(iterable, column_count):
    """
    Distribute items by columns, row-by-row.

    >>> tabulate([1, 2, 3, 4, 5], 2)
    [[1, 3, 5], [2, 4]]
    """
    columns = []
    for i in range(column_count):
        columns.append([])
    for i, item in enumerate(iterable):
        columns[i % column_count].append(item)
    return columns


def build_object_cache(obj_iter, key_attr_name):
    """
    Build object cache keyed by provided attribute name.
    Object key can be nullable (for interop keys), ignore these objects then.
    """
    obj_cache = dict()
    for obj in obj_iter:
        obj_key = getattr(obj, key_attr_name)
        if obj_key is not None and obj_key != u"":
            obj_cache[obj_key] = obj
    return obj_cache


def getattrs(obj, attr_names):
    attr_values = dict()
    for attr_name in attr_names:
        attr_values[attr_name] = getattr(obj, attr_name)
    return attr_values


TreeItem = collections.namedtuple('TreeItem', 'key data children parent_index')


def build_object_tree(obj_iter, item_key_producer, parent_key_producer, data_producer):
    """
    Build object tree based on parameters.

    >>> import collections
    >>> M = collections.namedtuple('M', 'id title parent')
    >>> build_object_tree([M(0, "i0", None), M(1, "i1", 0), M(2, "i2", 0), M(3, "i3", 2)],\
    lambda i: i.id, lambda i: i.parent, lambda i: dict(title=i.title))
    [TreeItem(key=0, data={'title': 'i0'}, children=[TreeItem(key=1, data={'title': 'i1'}, children=[], parent_index=0), TreeItem(key=2, data={'title': 'i2'}, children=[TreeItem(key=3, data={'title': 'i3'}, children=[], parent_index=0)], parent_index=0)], parent_index=0)]
    >>> build_object_tree([M(0, "i0", None), M(1, "i1", 0), M(2, "i2", 0), M(3, "i3", [0, 2])],\
    lambda i: i.id, lambda i: i.parent, lambda i: dict(title=i.title))
    [TreeItem(key=0, data={'title': 'i0'}, children=[TreeItem(key=1, data={'title': 'i1'}, children=[], parent_index=0), TreeItem(key=2, data={'title': 'i2'}, children=[TreeItem(key=3, data={'title': 'i3'}, children=[], parent_index=1)], parent_index=0), TreeItem(key=3, data={'title': 'i3'}, children=[], parent_index=0)], parent_index=0)]
    """
    parent_keys_cache = collections.OrderedDict()
    item_cache = dict()
    roots = []

    for obj in obj_iter:
        item_key = item_key_producer(obj)
        item = TreeItem(item_key, data_producer(obj), [], 0)
        item_cache[item_key] = item
        parent_key = parent_key_producer(obj)
        if parent_key is None:
            roots.append(item)
        else:
            parent_keys_cache[item_key] = parent_key

    for item_key, parent_key in six.iteritems(parent_keys_cache):
        item = item_cache[item_key]
        if isinstance(parent_key, collections.Iterable):
            for i, parent_key_instance in enumerate(parent_key):
                item_cache[parent_key_instance].children.append(item._replace(parent_index=i))
        else:
            item_cache[parent_key].children.append(item)

    return roots
