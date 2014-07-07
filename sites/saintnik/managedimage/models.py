# coding=utf-8
import os


def upload_path(pattern, params_extend=None):
    def resolve(instance, file_name):
        # Lower case is to avoid Linux/Windows file system case sensitivity difference.
        file_name, ext = os.path.splitext(file_name.lower())

        vars = instance.__dict__
        vars['file_name'] = file_name
        vars['class_path'] = model_class_path(instance)
        vars['ext'] = ext[1:]
        if params_extend:
            vars.update(getattr(instance, params_extend)())
        path = pattern.format(**vars) + ext
        return _build_path(path)
    return resolve

def model_class_path(instance):
    return u'-'.join([instance._meta.app_label, instance.__class__.__name__.lower()])

def _build_path(formatted_pattern):
    return os.path.join(*formatted_pattern.split(u'/'))
