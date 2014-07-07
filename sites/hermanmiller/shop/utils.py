# coding=utf-8
import re


def get_data_for_model(model, **kwargs):
    return {
        field.name: kwargs[field.name]
        for field in model._meta.local_fields
        if field.name != 'id' and field.name in kwargs
    }


def set_fields(obj, fields, update_keys=None):
    """Set fields of the object from the dictionary. Optinaly set of the keys to update can be restricted."""
    updated = False
    for key, val in fields.iteritems():
        if not update_keys or key in update_keys:
            if getattr(obj, key) != val:
                setattr(obj, key, val)
                updated = True
    return updated


def normalize_phone(text):
    return re.sub(r'[^0-9]+', '', text)
