# coding=utf-8
from sorl.thumbnail.templatetags.thumbnail import safe_filter, register, margin


@safe_filter(error_output='auto')
@register.filter
def hmargin(file_, geometry_string):
    """
    Returns the calculated margin for an image and geometry
    """
    result = margin(file_, geometry_string).split(' ')
    result[0] = result[2] = '0'
    return ' '.join(result)


@safe_filter(error_output='auto')
@register.filter
def vmargin(file_, geometry_string):
    """
    Returns the calculated margin for an image and geometry
    """
    result = margin(file_, geometry_string).split(' ')
    result[1] = result[3] = '0'
    return ' '.join(result)
