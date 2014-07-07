# coding=utf-8
import logging
import six
from django.db import transaction
from picassoft.utils.itertools import build_object_cache


def _is_special_name(name):
    return name.startswith('__') and name.endswith('__')


def object_update(obj, values):
    """
    Update object attributes from dictionary, skip special names like __attrs__.
    """
    changed = False
    for name, value in six.iteritems(values):
        if not _is_special_name(name) and hasattr(obj, name) and getattr(obj, name) != value:
            setattr(obj, name, value)
            changed = True
    return changed


def do_model_cud(model_type, model_key_name, values_iter, rebuild_parents=False):
    object_cache = build_object_cache(model_type.objects.all(), model_key_name)
    logging.debug(u"Started... [{}]".format(len(values_iter)))
    for values_dict in values_iter:
        obj_key = values_dict[model_key_name]
        obj_del = values_dict.get('__delete__', 'false').lower()
        if obj_del == 'true':
            obj = object_cache.get(obj_key)
            if obj is not None:
                obj.delete()
                logging.debug(u"Deleted object {}".format(obj_key))
        else:
            obj = object_cache.get(obj_key, model_type())
            if object_update(obj, values_dict):
                obj.save()
                object_cache[obj_key] = obj
                logging.debug(u"Saved object {}".format(obj_key))
            else:
                logging.debug(u"Skipped object {}".format(obj_key))

    if rebuild_parents:
        do_rebuild_parents(model_type, model_key_name, values_iter, object_cache)

    logging.debug(u"Transaction after parents rebuild: ".format(transaction.is_dirty()))


@transaction.commit_on_success
def do_rebuild_parents(model_type, model_key_name, values_iter, object_cache):
    with model_type.objects.disable_mptt_updates():
        for values_dict in values_iter:
            obj = object_cache[values_dict[model_key_name]]
            parent = object_cache.get(values_dict['__parent__'])
            obj.move_to(parent, position='last-child')
    model_type.objects.rebuild()
