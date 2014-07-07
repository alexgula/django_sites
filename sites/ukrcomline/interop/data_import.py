# coding=utf-8
from lxml import etree
from django.conf import settings
from .model_utils import do_model_cud
from catalog.models import Category


def get_category_elems(data):
    return (elem
            for elem in etree.ElementTree().parse(data)[0]
            if elem.tag == settings.XML_TAG_CATEGORY)


def prepare_elem_text(text):
    return text.replace(u"¶", u" ") if text else text


def load_data_from_xml(elem_iter, tag_map):
    """
    Loads iterable of element dictionaries from XML data.
    Attribute names are mapped in tag_map. Attributes not in map are ignored.
    """
    for elem in elem_iter:
        values_dict = {tag_map[attribute_elem.tag]: prepare_elem_text(attribute_elem.text)
                       for attribute_elem in elem
                       if attribute_elem.tag in tag_map}
        if values_dict['__parent__'] != u"00000000-0000-0000-0000-000000000000":  # skip top-level node
            yield values_dict


def load_categories(data):
    category_dicts = list(load_data_from_xml(get_category_elems(data), settings.XML_MAP_CATEGORY))
    do_model_cud(Category, 'interop_id', category_dicts, rebuild_parents=True)
