# coding=utf-8


def set_fields(obj, fields, update_keys=None):
    """Set fields of the object from the dictionary. Optinaly set of the keys to update can be restricted."""
    updated = False
    for key, val in fields.iteritems():
        if not update_keys or key in update_keys:
            if getattr(obj, key) != val:
                setattr(obj, key, val)
                updated = True
    return updated


def ensure_all_keys(fields, fmap, exclude_keys=None):
    """Check whether dictionary has all the keys of the map (for definition of the map see find_elem_children).
    Optional exclude_keys is a list of keys to exclude from the check.
    """
    for key, val in fmap.iteritems():
        if not (exclude_keys is None or val in exclude_keys or val in fields):
            return False
    return True


def map_dict(map, mapped_dict):
    return {val: mapped_dict[key] for key, val in map.iteritems()}


def update_model(model_class, model_filter, pk_getter, item_fields):
    """Update model items basing on dictionary."""

    updated = False

    for item in model_class.objects.filter(**model_filter):
        item_pk = pk_getter(item)
        if item_fields.has_key(item_pk):
            # Update existing
            if set_fields(item, item_fields[item_pk]):
                item.save()
                updated = True
            del item_fields[item_pk]
        else:
            # Delete missing
            item.delete()
            updated = True

    # Insert extra
    for fields in item_fields.itervalues():
        model_class.objects.create(**fields)
        updated = True

    return updated
