import os

from django.db import models


class ImageFieldManaged(models.ImageField):
    def __init__(self, verbose_name=None, name=None, field_name='image', **kwargs):
        self.field_name = field_name
        models.ImageField.__init__(self, verbose_name, name, upload_to=self.file_resolver(), **kwargs)

    def file_resolver(self):
        def resolve(instance, file_name):
            ext = os.path.splitext(file_name)[1]
            parts = instance.file_name_builder(self.field_name)
            base_path = os.path.join(*parts[:-1])
            file_name = ''.join((parts[-1], ext))
            return os.path.join(instance.__class__.__name__.lower(), base_path, file_name)
        return resolve

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ["^raisonne\.mediatools\.models\.ImageFieldManaged"])
