# coding=utf-8
from xml.etree.cElementTree import iterparse


def iter_elems(source, *args):
    """Get iterator to iterate over elements with given element tag.

    Parameters:
    *args -- contain path to the element, i.e. 'parent', 'child' means: find all elements with 'child' that are
        children of an element with tag 'parent'.
        N.B.! Child doesn't have to be immediate child if a parent. Thus children can be found on the different
        levels of the hierarchy.
        N.B.-2! Find only the first occurence of a parent.
    """
    context = iterparse(source, events=("start", "end"))
    context = iter(context)
    event, root = context.next()
    yield root

    def iter_elem(tag_name):
        """Iter over the terminal elements of the document."""
        for event, elem in context:
            if event == "end" and elem.tag == tag_name:
                yield elem
                root.clear()

    def iter_parent(*args):
        """Iter over parents of elements of the document if more than 1 argument else proxy iter_elem."""
        if len(args) == 1:
            for elem in iter_elem(args[0]):
                yield elem
        elif len(args) > 1:
            for event, elem in context:
                if event == "start" and elem.tag == args[0]:
                    for elem in iter_parent(*args[1:]):
                        yield elem
                    break  # Find only the first occurence of a parent.

    for elem in iter_parent(*args):
        yield elem


def find_elem_children(elem, attr_map):
    """Map element's immediate children text using the map given.

    Parameters:
    elem -- given element.
    map -- map of element's children tags to field codes. I.E., {"Tag": 'code'} will build dictionary item with key
        'code' and value of child with tag "Tag". If several children found, get only first.
    """
    res = dict()

    for child in elem:
        tag = child.tag
        text = child.text.strip() if child.text else u""
        if tag in attr_map and text and not attr_map[tag] in res:
            res[attr_map[tag]] = text

    return res
